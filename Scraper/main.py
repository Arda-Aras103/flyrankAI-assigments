import json
import os
import re
import socket
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from typing import Optional
from urllib.parse import urljoin, urlparse, urlunparse

from bs4 import BeautifulSoup
from pydantic import BaseModel, Field, ValidationError, field_validator

START_URL = "https://books.toscrape.com/catalogue/page-1.html"
MAX_PAGES = 3
CACHE_DIR = "cache"
OUTPUT_DIR = "output"
BOOKS_PATH = os.path.join(OUTPUT_DIR, "books.json")
ERRORS_PATH = os.path.join(OUTPUT_DIR, "errors.json")
REPORT_PATH = os.path.join(OUTPUT_DIR, "run-report.json")
USER_AGENT = "FlyRankInternship-A9/1.0 (+https://github.com/Arda-Aras103/flyrankAI-assigments)"
TIMEOUT_SECONDS = 10
DELAY_SECONDS = 0.5
RETRY_WAIT_SECONDS = 2

# Only for testing failure handling. Set it on the command line, never in the code.
EXTRA_BOOK_URL = os.environ.get("EXTRA_BOOK_URL")

RATING_WORDS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

_last_request_at = None
stats = {"pages_fetched": 0, "cache_hits": 0, "failed_pages": 0, "invalid_records": 0}


# ---------- Schema: the shape of a finished record ----------

class BookRecord(BaseModel):
    title: str = Field(min_length=1)
    product_url: str
    price_text: str
    price_gbp: float = Field(gt=0)
    availability_text: str = Field(min_length=1)
    rating_text: str
    rating_stars: int = Field(ge=1, le=5)
    description: Optional[str] = None
    source_page: str
    fetched_at: str

    @field_validator("product_url", "source_page")
    @classmethod
    def must_be_https(cls, value):
        if not value.startswith("https://"):
            raise ValueError("URL must start with https://")
        return value


# ---------- Politeness, fetching, caching ----------

def cache_path(name):
    return os.path.join(CACHE_DIR, name)


def polite_wait():
    global _last_request_at
    if _last_request_at is not None:
        wait = DELAY_SECONDS - (time.monotonic() - _last_request_at)
        if wait > 0:
            time.sleep(wait)
    _last_request_at = time.monotonic()


def fetch_page(url):
    """Returns (html, None) on success or (None, reason). Retries once, only on timeout or 5xx."""
    for attempt in (1, 2):
        polite_wait()
        try:
            request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
                if response.status == 200:
                    return response.read().decode("utf-8", errors="replace"), None
                reason = f"status {response.status}"
                retryable = False
        except urllib.error.HTTPError as e:
            reason = f"HTTP {e.code}"
            retryable = e.code >= 500
        except (urllib.error.URLError, TimeoutError) as e:
            inner = getattr(e, "reason", e)
            reason = f"request error: {inner}"
            retryable = isinstance(inner, (TimeoutError, socket.timeout))

        if not retryable or attempt == 2:
            return None, reason
        print(f"RETRY: {url} ({reason}), trying again in {RETRY_WAIT_SECONDS}s")
        time.sleep(RETRY_WAIT_SECONDS)
    return None, "unreachable"


def load_html(filename, url):
    """Returns (html, None) from cache or network, or (None, reason)."""
    path = cache_path(filename)

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()
        stats["cache_hits"] += 1
        print(f"CACHE HIT: {path} ({os.path.getsize(path)} bytes)")
        return html, None

    html, reason = fetch_page(url)
    if html is None:
        return None, reason

    stats["pages_fetched"] += 1
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"FETCH: saved {path} ({len(html.encode('utf-8'))} bytes)")
    return html, None


# ---------- Discovery ----------

def extract_book_links(html, page_url):
    soup = BeautifulSoup(html, "html.parser")

    book_links = []
    for anchor in soup.select("article.product_pod h3 a"):
        href = anchor.get("href")
        if href:
            book_links.append(urljoin(page_url, href))

    next_anchor = soup.select_one("li.next a")
    next_url = urljoin(page_url, next_anchor["href"]) if next_anchor else None

    return book_links, next_url


def canonical_url(url):
    parts = urlparse(url)
    return urlunparse((parts.scheme.lower(), parts.netloc.lower(), parts.path, "", "", ""))


def discover_catalogue():
    """Returns (unique (book_url, source_page) pairs, errors for pages that failed)."""
    pairs = []
    errors = []
    url = START_URL

    for page_number in range(1, MAX_PAGES + 1):
        html, reason = load_html(f"catalogue-page-{page_number}.html", url)
        if html is None:
            # Without this page we cannot find the next link, so discovery stops here.
            stats["failed_pages"] += 1
            errors.append({"product_url": url, "reason": f"catalogue page failed: {reason}"})
            print(f"FAILED: catalogue page {page_number}: {reason}")
            break

        links, next_url = extract_book_links(html, url)
        pairs.extend((link, url) for link in links)

        if page_number < MAX_PAGES:
            if next_url is None:
                break
            url = next_url

    if EXTRA_BOOK_URL:
        pairs.append((EXTRA_BOOK_URL, "manual test"))

    seen = set()
    unique = []
    for book_url, source_page in pairs:
        key = canonical_url(book_url)
        if key not in seen:
            seen.add(key)
            unique.append((book_url, source_page))
    return unique, errors


# ---------- Extraction ----------

def cache_name_for(book_url):
    path = urlparse(book_url).path.rstrip("/")
    slug = path.split("/")[-2] if path.endswith("index.html") else path.split("/")[-1]
    slug = re.sub(r"[^A-Za-z0-9_-]", "_", slug)
    return f"book-{slug}.html"


def text_or_none(node):
    if node is None:
        return None
    text = node.get_text(strip=True)
    return text or None


def parse_book(html, product_url, source_page, fetched_at):
    soup = BeautifulSoup(html, "html.parser")
    product = soup.select_one("article.product_page")
    if product is None:
        return None

    availability_node = product.select_one("div.product_main p.instock.availability")
    availability_text = (
        " ".join(availability_node.get_text(separator=" ", strip=True).split())
        if availability_node
        else None
    )

    rating_node = product.select_one("div.product_main p.star-rating")
    rating_text = None
    if rating_node:
        classes = [c for c in rating_node.get("class", []) if c != "star-rating"]
        rating_text = classes[0] if classes else None

    return {
        "title": text_or_none(product.select_one("div.product_main h1")),
        "product_url": product_url,
        "price_text": text_or_none(product.select_one("div.product_main p.price_color")),
        "availability_text": availability_text,
        "rating_text": rating_text,
        "description": text_or_none(product.select_one("#product_description + p")),
        "source_page": source_page,
        "fetched_at": fetched_at,
    }


# ---------- Normalization ----------

def normalize(raw):
    price_match = re.search(r"\d+(?:\.\d+)?", raw["price_text"] or "")
    if not price_match:
        raise ValueError(f"cannot read a price from {raw['price_text']!r}")

    rating_stars = RATING_WORDS.get(raw["rating_text"] or "")
    if rating_stars is None:
        raise ValueError(f"unknown rating {raw['rating_text']!r}")

    return {
        **raw,
        "product_url": canonical_url(raw["product_url"]),
        "price_gbp": float(price_match.group()),
        "rating_stars": rating_stars,
    }


# ---------- Per-book processing: one bad book never stops the run ----------

def file_fetched_at(path):
    ts = os.path.getmtime(path)
    return datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def format_validation_error(exc):
    return "; ".join(
        f"{'.'.join(str(part) for part in err['loc'])}: {err['msg']}"
        for err in exc.errors()
    )


def process_book(book_url, source_page):
    """Returns (record, None) or (None, error). Never raises on bad data."""
    key = canonical_url(book_url)
    filename = cache_name_for(book_url)

    html, reason = load_html(filename, book_url)
    if html is None:
        stats["failed_pages"] += 1
        return None, {"product_url": key, "reason": f"fetch failed: {reason}"}

    raw = parse_book(html, book_url, source_page, file_fetched_at(cache_path(filename)))
    if raw is None:
        stats["invalid_records"] += 1
        return None, {"product_url": key, "reason": "no product area found in page"}

    try:
        record = BookRecord(**normalize(raw))
    except ValidationError as exc:
        stats["invalid_records"] += 1
        return None, {"product_url": key, "reason": format_validation_error(exc)}
    except ValueError as exc:
        stats["invalid_records"] += 1
        return None, {"product_url": key, "reason": str(exc)}

    return record.model_dump(), None


def build_outputs():
    good_by_url = {}
    pairs, errors = discover_catalogue()

    for book_url, source_page in pairs:
        try:
            record, error = process_book(book_url, source_page)
        except Exception as exc:
            # Last line of defence: an unexpected bug in one book is logged, not fatal.
            stats["failed_pages"] += 1
            record, error = None, {"product_url": canonical_url(book_url), "reason": f"unexpected error: {exc!r}"}

        if error:
            errors.append(error)
            print(f"SKIPPED: {error['product_url']}: {error['reason']}")
            continue
        good_by_url[record["product_url"]] = record

    records = [good_by_url[url] for url in sorted(good_by_url)]
    return records, errors


# ---------- Output and run report ----------

def write_json(path, data):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, path)


def main():
    started_at = datetime.now(timezone.utc)
    t0 = time.monotonic()
    records, errors = [], []

    try:
        records, errors = build_outputs()
        write_json(BOOKS_PATH, records)
        write_json(ERRORS_PATH, errors)
    finally:
        report = {
            "started_at": started_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "duration_seconds": round(time.monotonic() - t0, 2),
            "pages_fetched": stats["pages_fetched"],
            "cache_hits": stats["cache_hits"],
            "valid_records": len(records),
            "invalid_records": stats["invalid_records"],
            "failed_pages": stats["failed_pages"],
        }
        write_json(REPORT_PATH, report)
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

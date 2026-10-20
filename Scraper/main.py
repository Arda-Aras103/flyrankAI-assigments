import json
import os
import re
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
USER_AGENT = "FlyRankInternship-A9/1.0 (+https://github.com/Arda-Aras103/flyrankAI-assigments)"
TIMEOUT_SECONDS = 10
DELAY_SECONDS = 0.5

RATING_WORDS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

_last_request_at = None


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


# ---------- Fetching and caching (unchanged from earlier stages) ----------

def cache_path(name):
    return os.path.join(CACHE_DIR, name)


def fetch_page(url):
    global _last_request_at

    if _last_request_at is not None:
        wait = DELAY_SECONDS - (time.monotonic() - _last_request_at)
        if wait > 0:
            time.sleep(wait)
    _last_request_at = time.monotonic()

    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            if response.status != 200:
                print(f"FAILED: {url} returned status {response.status}")
                return None
            return response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        print(f"FAILED: {url} returned HTTP {e.code}")
    except urllib.error.URLError as e:
        print(f"FAILED: request error for {url}: {e.reason}")
    return None


def load_html(filename, url):
    path = cache_path(filename)

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()
        print(f"CACHE HIT: {path} ({os.path.getsize(path)} bytes)")
        return html

    html = fetch_page(url)
    if html is None:
        return None

    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"FETCH: saved {path} ({len(html.encode('utf-8'))} bytes)")
    return html


# ---------- Discovery (unchanged from Stage 2) ----------

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


def discover_catalogue():
    pairs = []
    url = START_URL

    for page_number in range(1, MAX_PAGES + 1):
        html = load_html(f"catalogue-page-{page_number}.html", url)
        if html is None:
            break

        links, next_url = extract_book_links(html, url)
        pairs.extend((link, url) for link in links)

        if page_number < MAX_PAGES:
            if next_url is None:
                break
            url = next_url

    seen = set()
    unique = []
    for book_url, source_page in pairs:
        if book_url not in seen:
            seen.add(book_url)
            unique.append((book_url, source_page))
    return unique


# ---------- Extraction (unchanged from Stage 3) ----------

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


# ---------- Normalization: raw strings become clean values ----------

def canonical_url(url):
    parts = urlparse(url)
    return urlunparse((parts.scheme.lower(), parts.netloc.lower(), parts.path, "", "", ""))


def normalize(raw):
    """Adds clean values next to the raw ones. Raises ValueError if a value can't be understood."""
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


# ---------- Validation and storage ----------

def format_validation_error(exc):
    return "; ".join(
        f"{'.'.join(str(part) for part in err['loc'])}: {err['msg']}"
        for err in exc.errors()
    )


def file_fetched_at(path):
    ts = os.path.getmtime(path)
    return datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def write_json(path, data):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, path)


def build_outputs():
    """Builds good records and errors from scratch on every run, so re-runs never duplicate."""
    good_by_url = {}
    errors = []

    for book_url, source_page in discover_catalogue():
        key = canonical_url(book_url)
        if key in good_by_url:
            continue

        html = load_html(cache_name_for(book_url), book_url)
        if html is None:
            errors.append({"product_url": book_url, "reason": "fetch failed"})
            continue

        fetched_at = file_fetched_at(cache_path(cache_name_for(book_url)))
        raw = parse_book(html, book_url, source_page, fetched_at)
        if raw is None:
            errors.append({"product_url": book_url, "reason": "no product area found in page"})
            continue

        try:
            record = BookRecord(**normalize(raw))
        except ValidationError as exc:
            errors.append({"product_url": key, "reason": format_validation_error(exc)})
            continue
        except ValueError as exc:
            errors.append({"product_url": key, "reason": str(exc)})
            continue

        good_by_url[key] = record.model_dump()

    records = [good_by_url[url] for url in sorted(good_by_url)]
    return records, errors


def main():
    records, errors = build_outputs()

    write_json(BOOKS_PATH, records)
    write_json(ERRORS_PATH, errors)

    print(f"records={len(records)}")
    print(f"errors={len(errors)}")
    print(f"wrote {BOOKS_PATH} and {ERRORS_PATH}")


if __name__ == "__main__":
    main()

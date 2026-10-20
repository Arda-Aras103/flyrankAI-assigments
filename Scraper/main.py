import os
import re
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

START_URL = "https://books.toscrape.com/catalogue/page-1.html"
MAX_PAGES = 3
CACHE_DIR = "cache"
USER_AGENT = "FlyRankInternship-A9/1.0 (+https://github.com/Arda-Aras103/flyrankAI-assigments)"
TIMEOUT_SECONDS = 10
DELAY_SECONDS = 0.5

_last_request_at = None


def cache_path(name):
    return os.path.join(CACHE_DIR, name)


def fetch_page(url):
    """Makes a real request to the site, respecting the delay between requests."""
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
    """Returns HTML from cache if present, otherwise fetches and caches it."""
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


def extract_book_links(html, page_url):
    """Returns absolute book URLs and the absolute URL of the next page, if any."""
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
    """Returns a list of (book_url, source_page_url) pairs, de-duplicated by book_url."""
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


def cache_name_for(book_url):
    """Builds a filename from the book's URL path, e.g. a-light-in-the-attic_1000.html."""
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

    title = text_or_none(product.select_one("div.product_main h1"))

    price_text = text_or_none(product.select_one("div.product_main p.price_color"))

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

    description_node = product.select_one("#product_description + p")
    description = text_or_none(description_node)

    return {
        "title": title,
        "product_url": product_url,
        "price_text": price_text,
        "availability_text": availability_text,
        "rating_text": rating_text,
        "description": description,
        "source_page": source_page,
        "fetched_at": fetched_at,
    }


def main():
    catalogue = discover_catalogue()
    records = []
    skipped = 0

    for book_url, source_page in catalogue:
        html = load_html(cache_name_for(book_url), book_url)
        if html is None:
            skipped += 1
            continue

        fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        record = parse_book(html, book_url, source_page, fetched_at)
        if record is None:
            print(f"FAILED: no product area found in {book_url}")
            skipped += 1
            continue
        records.append(record)

    if records:
        print("Sample record:")
        for key, value in records[0].items():
            print(f"  {key}: {value!r}")

    print(f"detail_pages={len(records)}")
    if skipped:
        print(f"skipped={skipped}")


if __name__ == "__main__":
    main()

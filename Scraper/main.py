import os
import time
import urllib.request
import urllib.error
from urllib.parse import urljoin

from bs4 import BeautifulSoup

START_URL = "https://books.toscrape.com/catalogue/page-1.html"
MAX_PAGES = 3
CACHE_DIR = "cache"
USER_AGENT = "FlyRankInternship-A9/1.0 (+https://github.com/Arda-Aras103/flyrankAI-assigments)"
TIMEOUT_SECONDS = 10
DELAY_SECONDS = 0.5

_last_request_at = None


def cache_path(page_number):
    return os.path.join(CACHE_DIR, f"catalogue-page-{page_number}.html")


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


def load_page(page_number, url):
    """Returns HTML from cache if present, otherwise fetches and caches it."""
    path = cache_path(page_number)

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


def main():
    all_links = []
    pages_done = 0
    url = START_URL

    for page_number in range(1, MAX_PAGES + 1):
        html = load_page(page_number, url)
        if html is None:
            break

        pages_done += 1
        links, next_url = extract_book_links(html, url)
        all_links.extend(links)

        if page_number < MAX_PAGES:
            if next_url is None:
                break
            url = next_url

    unique_links = list(dict.fromkeys(all_links))

    print(f"catalogue_pages={pages_done}")
    print(f"discovered={len(all_links)}")
    print(f"unique_urls={len(unique_links)}")


if __name__ == "__main__":
    main()

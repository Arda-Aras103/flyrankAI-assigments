import os
import urllib.request
import urllib.error

CATALOGUE_URL = "https://books.toscrape.com/catalogue/page-1.html"
CACHE_DIR = "cache"
CACHE_PATH = os.path.join(CACHE_DIR, "catalogue-page-1.html")
USER_AGENT = "FlyRankInternship-A9/1.0 (+https://github.com/Arda-Aras103/flyrankAI-assigments)"
TIMEOUT_SECONDS = 10


def fetch_page():
    request = urllib.request.Request(CATALOGUE_URL, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            if response.status != 200:
                print(f"FAILED: status {response.status}, nothing saved")
                return None
            return response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        print(f"FAILED: HTTP {e.code}, nothing saved")
    except urllib.error.URLError as e:
        print(f"FAILED: request error: {e.reason}")
    return None


def save_page(html):
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        f.write(html)


def main():
    if os.path.exists(CACHE_PATH):
        size = os.path.getsize(CACHE_PATH)
        print(f"CACHE HIT: {CACHE_PATH} ({size} bytes)")
        return

    html = fetch_page()
    if html is None:
        return

    save_page(html)
    size = len(html.encode("utf-8"))
    print(f"FETCH: saved {CACHE_PATH} ({size} bytes)")


if __name__ == "__main__":
    main()

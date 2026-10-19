import urllib.request
import urllib.error
from datetime import datetime, timezone

ROBOTS_URL = "https://books.toscrape.com/robots.txt"


def check_robots():
    try:
        with urllib.request.urlopen(ROBOTS_URL, timeout=10) as response:
            body = response.read().decode("utf-8", errors="replace")
            print(f"Status: {response.status}")
            print(body)
    except urllib.error.HTTPError as e:
        print(f"Status: {e.code}")
        print("no robots file found")
    except urllib.error.URLError as e:
        print(f"Request failed: {e.reason}")



if __name__ == "__main__":
    check_robots()

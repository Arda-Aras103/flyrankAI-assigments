# Books to Scrape: Scraper

A small Python scraper that collects the first three catalogue pages of
https://books.toscrape.com, opens each book's detail page, cleans the values,
validates them against a schema, and writes `books.json` plus a run report.

## Target classification

- **Site:** books.toscrape.com
- **Why this site:** It is a sandbox built for practising web scraping. The site
  says so on its own pages (checked on [DATE]).
- **robots.txt:** I requested https://books.toscrape.com/robots.txt on [DATE].
  Result: [status code and body, or "no robots file found"].
- **How much:** The first 3 catalogue pages only (60 books).
- **Data collected:** Title, price, availability, star rating, and description
  from the listing and detail pages. Nothing else.
- **Why this is appropriate:** The site is built for this purpose, and the scope
  is limited to three pages.

I will not reuse this code on another site without checking its rules and terms first.

## Lane and install

Python 3. Tested on Linux (WSL Ubuntu).

```bash
git clone https://github.com/Arda-Aras103/flyrankAI-assigments.git
cd flyrankAI-assigments/Scraper
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
cd Scraper && source .venv/bin/activate && python3 main.py
```

On a cold run (empty `cache/`) the scraper makes about 63 requests with a
0.5 second delay between them. On later runs it reads from `cache/` and makes
no requests.

Outputs:
- `output/books.json`: the valid records (60 expected)
- `output/errors.json`: records that failed, with reasons
- `output/run-report.json`: start time, duration, and counts for this run

## Record schema

| Field | Type | Required | Notes |
|---|---|---|---|
| `title` | string | yes | Non-empty |
| `product_url` | string | yes | Canonical absolute `https://` URL. Used as identity. |
| `price_text` | string | yes | Raw text, e.g. `£51.77` |
| `price_gbp` | number | yes | Parsed from `price_text`, greater than 0 |
| `availability_text` | string | yes | Raw text, e.g. `In stock (22 available)` |
| `rating_text` | string | yes | Raw word, e.g. `Three` |
| `rating_stars` | integer | yes | 1 to 5, mapped from `rating_text` |
| `description` | string or null | no | `null` if the page has no description |
| `source_page` | string | yes | `https://` URL of the catalogue page the book was found on |
| `fetched_at` | string | yes | UTC timestamp, ISO 8601 |

Validation is done with Pydantic. Records that fail go to `errors.json`, never to `books.json`.

## Politeness rules

- **User-Agent:** `FlyRankInternship-A9/1.0 (+https://github.com/Arda-Aras103/flyrankAI-assigments)` on every request.
- **Delay:** at least 0.5 seconds between real requests. Cached pages cause no request and no delay.
- **Timeout:** 10 seconds per request.
- **Retries:** one retry, only for timeouts and 5xx responses. No retry for 404 or 403.
- **Cache:** every page is saved under `cache/` the first time it is fetched. Later runs read the saved copy.

## Why no browser

The product data is already in the HTML the server sends, so a plain HTTP request
and an HTML parser are enough. A headless browser would add cost and
complexity without adding any data.

## Ethics

Use an official API when one exists. Do not bypass logins, paywalls, or blocks.
Collect only the fields the task needs.

## Limitations

`fetched_at` is taken from the modification time of the cached file, not from
the moment of the request. For a fresh fetch these are almost the same, but after
a cache is copied or touched the value can drift. A proper fix would store the
request time inside the cache.

## Proof: a real run

This is the `run-report.json` from a run with a warm cache and no failures:

```json
{
  "started_at": "2026-10-20T14:59:32Z",
  "duration_seconds": 0.53,
  "pages_fetched": 0,
  "cache_hits": 63,
  "valid_records": 60,
  "invalid_records": 0,
  "failed_pages": 0
}
```

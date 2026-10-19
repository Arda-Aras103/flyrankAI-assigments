# Scraper

## Target classification

- **Site:** https://books.toscrape.com
- **Why this site:** toscrape.com describes Books to Scrape as "a fictional bookstore that desperately wants to be scraped" and "a safe place for beginners learning web scraping." It is a practice sandbox built for this purpose.
- **How much:** the first 3 catalogue pages only (pages 1 to 3, up to 60 books).
- **Data collected:** book title, price, star rating, and availability, for the books listed on those 3 pages.
- **Why this is appropriate:** the site states in its own words that it exists for scraping practice, and the scope is limited to a small sample.

### robots.txt check

- Request: `GET https://books.toscrape.com/robots.txt`
- Result: HTTP 404. No robots file found.
- Note: a missing robots file is not permission. It only means the site publishes no crawling instructions. The sandbox statement above is the basis for scraping here.

### Checkpoint

- Target: books.toscrape.com
- Scope: first 3 catalogue pages
- robots result: 404, no robots file found

I will not reuse this code on another site without checking its rules and terms first.

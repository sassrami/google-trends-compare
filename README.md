# Compare more than 5 keywords in Google Trends (pytrends alternative)

Google Trends compares at most 5 keywords at a time, and every request rescales its own top value to 100. Split 12 keywords into batches of 5 and the numbers from different batches can't be compared. On top of that, pytrends is archived and Google answers scripts with HTTP 429.

`compare.py` gets interest over time for **any number of keywords on one shared 0-100 scale** and writes a CSV with one column per keyword. It calls a hosted Google Trends scraper on Apify, so there is no rate limiting, cookie handling or proxy setup on your side.

```bash
pip install apify-client
export APIFY_TOKEN=...   # free account at https://apify.com (Settings > API & Integrations)
                         # Windows PowerShell: $env:APIFY_TOKEN = "..."
python compare.py sneakers "running shoes" "trail running shoes" "barefoot shoes" \
  "wide toe box shoes" "minimalist shoes" "walking shoes" "hiking boots" "waterproof shoes" \
  "cross training shoes" "carbon plate running shoes" "zero drop shoes" --geo US
```

Output (`trends.csv`, real data, US, last 12 months):

| date | sneakers | hiking boots | walking shoes | barefoot shoes | zero drop shoes |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2025-11-02 | 24 | 1.78 | 2.3 | 0.92 | 0.21 |
| 2025-11-09 | 25 | 1.88 | 2.3 | 0.92 | 0.21 |
| 2025-11-16 | 28 | 2.3 | 2.3 | 0.92 | 0.21 |

All columns share one scale: averaged over the year, "sneakers" (35.4) is about 160 times "zero drop shoes" (0.22). Fetched in separate batches of 5, those two numbers would come from different scales and could not be compared.

Options: `--geo` (country code, empty = worldwide), `--time` (`today 5-y`, `now 7-d`, `2024-01-01 2024-12-31`, ...), `--out` (CSV path).

## Cost

The scraper charges per result: one keyword's time series is one result, $0.002 or less. 50 keywords cost about $0.10. Keywords Google has no data for are not charged. Apify's free plan includes monthly credit that covers small runs.

## Why not pytrends?

pytrends was archived on GitHub in 2025. Google rate-limits Trends per IP, and datacenter and cloud IPs (Colab, AWS, CI) often get 429 on the first request. If you want to keep doing it yourself: a few seconds between requests, a fresh session after each 429, exponential backoff, and residential IPs for volume.

## Disclosure

I built and maintain the scraper this calls: [granola2/google-trends-scraper](https://apify.com/granola2/google-trends-scraper). It also returns related queries, interest by region and trending searches. This script is MIT licensed.

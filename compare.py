"""Compare any number of keywords on one Google Trends 0-100 scale.

Usage:
    export APIFY_TOKEN=...            # free account at apify.com
    python compare.py pickleball padel tennis squash badminton golf --geo US

Writes trends.csv: one row per date, one column per keyword, all on one scale.
"""

import argparse
import csv
import os

from apify_client import ApifyClient

ACTOR = "granola2/google-trends-scraper"


def to_table(items: list[dict]) -> tuple[list[str], list[list]]:
    """Turn the Actor's interestOverTime rows into a header and date-sorted rows."""
    series = [i for i in items if i.get("report") == "interestOverTime"]
    keywords = [s["keyword"] for s in series]
    by_date: dict[str, dict] = {}
    for s in series:
        for p in s["points"]:
            by_date.setdefault(p["date"], {})[s["keyword"]] = p["value"]
    rows = [[d] + [by_date[d].get(k, "") for k in keywords] for d in sorted(by_date)]
    return ["date", *keywords], rows


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("keywords", nargs="+")
    ap.add_argument("--geo", default="", help="country code like US or DE; empty = worldwide")
    ap.add_argument("--time", default="today 12-m", help="e.g. 'today 5-y', 'now 7-d', '2024-01-01 2024-12-31'")
    ap.add_argument("--out", default="trends.csv")
    args = ap.parse_args()

    client = ApifyClient(os.environ["APIFY_TOKEN"])
    run = client.actor(ACTOR).call(
        run_input={"keywords": args.keywords, "geo": args.geo, "timeRange": args.time, "reports": ["interestOverTime"]}
    )
    items = client.dataset(run.default_dataset_id).list_items().items
    header, rows = to_table(items)
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows([header, *rows])
    missing = set(args.keywords) - set(header)
    print(f"Wrote {len(rows)} dates x {len(header) - 1} keywords to {args.out}")
    if missing:
        print("No Google Trends data for:", ", ".join(sorted(missing)))


if __name__ == "__main__":
    main()

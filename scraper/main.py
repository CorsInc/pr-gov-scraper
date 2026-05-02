"""Main entry point for pr.gov scraper."""

import json
import os
import time
from pathlib import Path

import requests

from scraper.config import BASE_URL, HEADERS, REQUEST_DELAY, OUTPUT_DIR, SECTIONS
from scraper.parsers import parse_main_page, parse_generic_page


def fetch(url: str) -> str | None:
    """Fetch a URL with rate limiting and error handling."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        return resp.text
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch {url}: {e}")
        return None


def save_json(data: dict, filename: str):
    """Save data as JSON to the output directory."""
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[OK] Saved {path}")


def scrape_all():
    """Scrape all configured sections of pr.gov."""
    print(f"Starting scrape of {BASE_URL}")
    results = {}

    for name, path in SECTIONS.items():
        url = f"{BASE_URL}{path}"
        print(f"\n--- Scraping {name}: {url} ---")
        html = fetch(url)
        if not html:
            continue

        if name == "main":
            data = parse_main_page(html)
        else:
            data = parse_generic_page(html)

        results[name] = data
        save_json(data, f"{name}.json")
        time.sleep(REQUEST_DELAY)

    # Save full report
    save_json(results, "full_report.json")
    print(f"\nDone! Scraped {len(results)} sections.")
    return results


def scrape_section(section: str) -> dict | None:
    """Scrape a single section by key (e.g. 'agencies', 'news')."""
    if section not in SECTIONS:
        print(f"[ERROR] Unknown section '{section}'. Options: {list(SECTIONS.keys())}")
        return None

    url = f"{BASE_URL}{SECTIONS[section]}"
    html = fetch(url)
    if not html:
        return None

    data = parse_generic_page(html)
    save_json(data, f"{section}.json")
    return data


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        scrape_section(sys.argv[1])
    else:
        scrape_all()

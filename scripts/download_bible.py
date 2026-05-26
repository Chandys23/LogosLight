"""
download_bible.py
Downloads the KJV Bible JSON from scrollmapper/bible_databases (public domain).
Run once before load_verses.py.
"""

import json
import requests

URL = "https://raw.githubusercontent.com/scrollmapper/bible_databases/master/json/bible-en-kjv.json"
OUT = "bible-kjv.json"


def main():
    print("Downloading KJV Bible (public domain)...")
    response = requests.get(URL, timeout=60)
    response.raise_for_status()
    data = response.json()
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f)
    print(f"Saved to {OUT}")
    total = sum(len(v) for b in data for v in b["chapters"])
    print(f"Books: {len(data)}  |  Verses: {total:,}")


if __name__ == "__main__":
    main()

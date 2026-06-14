"""
download_bible.py
Downloads the KJV Bible JSON from a reliable public API.
Run once before load_verses.py.
"""

import json
import requests

# Using Get Bible API - free, reliable, no auth needed
# Returns verses in format: {"book": "Genesis", "chapter": 1, "verse": 1, "text": "..."}
BASE_URL = "https://api.getbible.com/v2/bible/kjv.json"
OUT = "bible-kjv.json"


def main():
    print("Downloading KJV Bible (public domain)...")
    response = requests.get(BASE_URL, timeout=60)
    response.raise_for_status()
    data = response.json()
    
    # Extract Bible book data
    bible_data = data.get("data", data)
    
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(bible_data, f)
    
    print(f"Saved to {OUT}")
    
    # Count total verses
    total = 0
    for book_name, book_data in bible_data.items():
        if isinstance(book_data, dict) and "chapters" in book_data:
            for chapter in book_data["chapters"].values():
                total += len(chapter) if isinstance(chapter, list) else len(chapter.get("verses", []))
    
    print(f"Books: {len(bible_data)}  |  Verses: ~{total:,}")


if __name__ == "__main__":
    main()

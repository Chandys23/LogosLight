"""
load_verses.py
Loads all 31,102 KJV verses from bible-kjv.json into Supabase.
Run once after download_bible.py and after creating the verses table in Supabase.

Required Supabase SQL (run in SQL Editor first):

    CREATE TABLE verses (
        id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        book         VARCHAR(50)  NOT NULL,
        chapter      INT          NOT NULL,
        verse_number INT          NOT NULL,
        text         TEXT         NOT NULL,
        version      VARCHAR(10)  DEFAULT 'KJV',
        created_at   TIMESTAMP    DEFAULT NOW(),
        UNIQUE (book, chapter, verse_number)
    );

    CREATE INDEX idx_verses_ref ON verses(book, chapter, verse_number);

    CREATE OR REPLACE FUNCTION get_random_verse()
    RETURNS TABLE(book VARCHAR, chapter INT, verse_number INT, text TEXT)
    LANGUAGE sql AS $$
        SELECT book, chapter, verse_number, text FROM verses ORDER BY RANDOM() LIMIT 1;
    $$;
"""

import json
import os
import sys
import time

from dotenv import load_dotenv
from supabase import create_client

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "backend", ".env"))

BIBLE_JSON = os.path.join(os.path.dirname(__file__), "bible-kjv.json")
BATCH_SIZE = 500


def main():
    url = os.getenv("SUPABASE_URL")
    # Use service role key for loading (bypasses RLS on INSERT)
    # Falls back to SUPABASE_KEY if service role key not set
    key = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_KEY")
    if not url or not key:
        print("ERROR: SUPABASE_URL and SUPABASE_KEY must be set in backend/.env")
        sys.exit(1)

    if not os.path.exists(BIBLE_JSON):
        print(f"ERROR: {BIBLE_JSON} not found. Run download_bible.py first.")
        sys.exit(1)

    supabase = create_client(url, key)

    print("LogosLight KJV Loader\n")
    with open(BIBLE_JSON, encoding="utf-8") as f:
        data = json.load(f)

    verses = []
    total_books = len(data)
    for i, book in enumerate(data, 1):
        print(f"  Parsing [{i:2}/{total_books}] {book['name']}")
        for ch_num, chapter in enumerate(book["chapters"], 1):
            for v_num, text in enumerate(chapter, 1):
                if text.strip():
                    verses.append({
                        "book":         book["name"],
                        "chapter":      ch_num,
                        "verse_number": v_num,
                        "text":         text.strip(),
                        "version":      "KJV",
                    })

    print(f"\nParsed {len(verses):,} verses")

    # Check existing count
    existing = supabase.table("verses").select("id", count="exact").execute().count
    if existing and existing > 0:
        print(f"Table already has {existing:,} rows. Skipping insert.")
        return

    batches = (len(verses) + BATCH_SIZE - 1) // BATCH_SIZE
    print(f"Inserting in {batches} batches of {BATCH_SIZE}...\n")

    for n, i in enumerate(range(0, len(verses), BATCH_SIZE), 1):
        batch = verses[i : i + BATCH_SIZE]
        supabase.table("verses").insert(batch).execute()
        pct = int(n / batches * 100)
        print(f"  Batch {n:3}/{batches} ({pct:3}%) ✓")
        time.sleep(0.2)  # gentle rate limiting

    # Final verification
    count = supabase.table("verses").select("id", count="exact").execute().count
    print(f"\nDatabase now has {count:,} verses")
    if count == 31102:
        print("All 31,102 KJV verses loaded successfully!")
    else:
        print(f"Warning: expected 31,102 but got {count:,}. Check for duplicates.")


if __name__ == "__main__":
    main()

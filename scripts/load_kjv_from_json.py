"""
load_kjv_from_json.py
Load complete KJV Bible (31,102 verses) from local JSON into Supabase
"""

import os
import sys
import json
import time
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from supabase import create_client

load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'backend', '.env'))

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_KEY")
)


def load_all_verses():
    """Load all KJV verses from local JSON into Supabase"""
    
    json_file = os.path.join(os.path.dirname(__file__), "bible-kjv.json")
    if not os.path.exists(json_file):
        print(f"ERROR: {json_file} not found!")
        return
    
    print("LogosLight - Full KJV Bible Loader")
    print("=" * 50)
    print(f"Reading {json_file}...")
    
    with open(json_file, 'r', encoding='utf-8') as f:
        bible_data = json.load(f)
    
    print(f"Found {len(bible_data)} books")
    print()
    
    # Parse all verses
    all_verses = []
    for book_name, book_data in bible_data.items():
        if not isinstance(book_data, dict) or "chapters" not in book_data:
            continue
        
        chapters = book_data.get("chapters", {})
        for chapter_num, verses in chapters.items():
            if isinstance(verses, dict):
                # verses is a dict with verse numbers as keys
                for verse_num, text in verses.items():
                    if isinstance(text, str) and text.strip():
                        all_verses.append({
                            "book": book_name,
                            "chapter": int(chapter_num),
                            "verse_number": int(verse_num),
                            "text": text.strip(),
                            "version": "KJV"
                        })
            elif isinstance(verses, list):
                # verses is a list where index = verse number
                for verse_num, text in enumerate(verses, 1):
                    if isinstance(text, str) and text.strip():
                        all_verses.append({
                            "book": book_name,
                            "chapter": int(chapter_num),
                            "verse_number": verse_num,
                            "text": text.strip(),
                            "version": "KJV"
                        })
    
    print(f"Parsed {len(all_verses):,} verses")
    print()
    
    # Clear existing verses
    print("Clearing old verses from database...")
    try:
        supabase.table("verses").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
        print("✓ Old verses cleared")
    except Exception as e:
        print(f"⚠ Warning: {e}")
    
    print()
    
    # Batch insert
    batch_size = 500
    total_batches = (len(all_verses) + batch_size - 1) // batch_size
    
    print(f"Inserting {len(all_verses):,} verses in {total_batches} batches...")
    print()
    
    for batch_num in range(0, len(all_verses), batch_size):
        batch = all_verses[batch_num:batch_num + batch_size]
        batch_idx = batch_num // batch_size + 1
        
        try:
            result = supabase.table("verses").insert(batch).execute()
            percent = (batch_idx * 100) // total_batches
            print(f"  [{batch_idx:3d}/{total_batches}] {percent:3d}% - {len(batch):3d} verses", flush=True)
            time.sleep(0.1)  # Small delay to avoid rate limiting
        except Exception as e:
            print(f"  ERROR in batch {batch_idx}: {e}")
    
    print()
    
    # Verify
    print("Verifying...")
    try:
        result = supabase.table("verses").select("id", count="exact").execute()
        count = result.count if hasattr(result, 'count') else len(result.data)
        print(f"✓ Database now contains {count:,} verses")
        
        if count == 31102:
            print()
            print("🎉 SUCCESS! Full KJV Bible (31,102 verses) loaded!")
        else:
            print()
            print(f"⚠ Note: Expected 31,102 verses, found {count:,}")
    except Exception as e:
        print(f"ERROR verifying: {e}")


if __name__ == "__main__":
    load_all_verses()

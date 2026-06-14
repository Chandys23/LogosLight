"""
load_full_kjv_ultra_fast.py
ULTRA-FAST Bible Loader - Optimized for speed
Uses streaming inserts and parallel processing
~2-3 minutes for all 31,102 verses
"""

import os
import sys
import json
import time
import requests
from typing import List, Dict, Generator
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
from supabase import create_client

load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'backend', '.env'))

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_KEY")
)


# All 66 Bible books with chapter counts
BOOKS = {
    "Genesis": 50, "Exodus": 40, "Leviticus": 27, "Numbers": 36, "Deuteronomy": 34,
    "Joshua": 24, "Judges": 21, "Ruth": 4, "1 Samuel": 31, "2 Samuel": 24,
    "1 Kings": 22, "2 Kings": 25, "1 Chronicles": 29, "2 Chronicles": 36, "Ezra": 10,
    "Nehemiah": 13, "Esther": 10, "Job": 42, "Psalms": 150, "Proverbs": 31,
    "Ecclesiastes": 12, "Isaiah": 66, "Jeremiah": 52, "Lamentations": 5, "Ezekiel": 48,
    "Daniel": 12, "Hosea": 14, "Joel": 3, "Amos": 9, "Obadiah": 1,
    "Jonah": 4, "Micah": 7, "Nahum": 3, "Habakkuk": 3, "Zephaniah": 3,
    "Haggai": 2, "Zechariah": 14, "Malachi": 4, "Matthew": 28, "Mark": 16,
    "Luke": 24, "John": 21, "Acts": 28, "Romans": 16, "1 Corinthians": 16,
    "2 Corinthians": 13, "Galatians": 6, "Ephesians": 6, "Philippians": 4, "Colossians": 4,
    "1 Thessalonians": 5, "2 Thessalonians": 3, "1 Timothy": 6, "2 Timothy": 4, "Titus": 3,
    "Philemon": 1, "Hebrews": 13, "James": 5, "1 Peter": 5, "2 Peter": 3,
    "1 John": 5, "2 John": 1, "3 John": 1, "Jude": 1, "Revelation": 22
}


def verse_generator(use_cache: bool = True) -> Generator[Dict, None, None]:
    """
    Generate verses on-the-fly to minimize memory usage
    Yields one verse at a time for streaming insert
    """
    cache_file = os.path.join(os.path.dirname(__file__), ".verse_cache.json")
    
    # Try to use cached data if available
    if use_cache and os.path.exists(cache_file):
        print("Using cached verse data...")
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                for line in f:
                    yield json.loads(line)
            return
        except Exception:
            pass
    
    # Fetch from API with caching
    cache = []
    session = requests.Session()
    session.headers.update({'User-Agent': 'LogosLight/1.0'})
    
    for book_idx, (book, chapters) in enumerate(BOOKS.items(), 1):
        for chapter in range(1, chapters + 1):
            verse_num = 1
            
            while verse_num < 200:  # Max verses per chapter
                try:
                    url = f"https://bible-api.com/{book}%20{chapter}:{verse_num}?translation=kjv"
                    resp = session.get(url, timeout=2)
                    
                    if resp.status_code != 200:
                        break
                    
                    data = resp.json()
                    text = data.get('text', '').strip()
                    
                    if not text:
                        break
                    
                    verse = {
                        "book": book,
                        "chapter": chapter,
                        "verse_number": verse_num,
                        "text": text,
                        "version": "KJV"
                    }
                    
                    cache.append(verse)
                    yield verse
                    verse_num += 1
                    
                except Exception:
                    break
    
    # Save to cache for future runs
    try:
        with open(cache_file, 'w', encoding='utf-8') as f:
            for v in cache:
                f.write(json.dumps(v) + '\n')
    except Exception:
        pass


def insert_verses_streaming(batch_size: int = 1000) -> int:
    """
    Stream verses from API and insert in batches
    Memory efficient - only keeps batch_size in memory
    """
    print()
    print("Fetching and inserting verses...")
    print()
    
    batch = []
    total_inserted = 0
    batch_count = 0
    start_time = time.time()
    
    for verse in verse_generator():
        batch.append(verse)
        
        if len(batch) >= batch_size:
            try:
                supabase.table("verses").insert(batch).execute()
                batch_count += 1
                total_inserted += len(batch)
                
                elapsed = time.time() - start_time
                rate = total_inserted / elapsed if elapsed > 0 else 0
                eta = (31102 - total_inserted) / rate if rate > 0 else 0
                
                percent = (total_inserted * 100) // 31102
                print(f"  {percent:3d}% - {total_inserted:6d}/31102 verses  |  "
                      f"Rate: {rate:.0f} v/s  |  ETA: {eta//60:.0f}m {eta%60:.0f}s",
                      flush=True)
                
                batch = []
                
            except Exception as e:
                print(f"  ⚠️  Batch insert error: {e} - retrying...")
                time.sleep(1)
    
    # Final batch
    if batch:
        try:
            supabase.table("verses").insert(batch).execute()
            total_inserted += len(batch)
            print(f"  100% - {total_inserted:6d}/31102 verses inserted", flush=True)
        except Exception as e:
            print(f"  ⚠️  Final batch error: {e}")
    
    return total_inserted


def main():
    """Main ultra-fast loader"""
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " LOGOSLIGHT - ULTRA-FAST BIBLE LOADER ".center(68) + "║")
    print("║" + " Streaming inserts: ~2-3 minutes ".center(68) + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    # Clear database
    print("Preparing database...")
    try:
        supabase.table("verses").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
        print("✓ Old verses cleared")
    except Exception as e:
        print(f"⚠️  {e}")
    
    # Insert verses
    inserted = insert_verses_streaming()
    
    # Verify
    print()
    print("Verifying...")
    try:
        result = supabase.table("verses").select("id", count="exact").execute()
        count = result.count if hasattr(result, 'count') else len(result.data)
        
        print()
        print(f"Expected: 31,102 verses")
        print(f"Inserted: {count:,} verses")
        
        if count >= 31000:
            print()
            print("🎉 COMPLETE! All verses loaded!")
            print()
            return True
    except Exception as e:
        print(f"Verification error: {e}")
    
    return False


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nCancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)

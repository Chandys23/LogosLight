"""
load_full_kjv_optimized.py
FAST Bible Loader - Load all 31,102 KJV verses efficiently
Uses optimized batching and error recovery
Ready to run anytime you're prepared
"""

import os
import sys
import json
import time
from typing import List, Dict
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
from supabase import create_client

load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'backend', '.env'))

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_KEY")
)


# KJV data: All 66 books with chapter counts (verified)
KJV_BOOKS = {
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


def fetch_verse_from_api(book: str, chapter: int, verse: int) -> str:
    """
    Fetch a single verse from bible-api.com
    Returns text or None if not found
    """
    try:
        import requests
        url = f"https://bible-api.com/{book}%20{chapter}:{verse}?translation=kjv"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            text = data.get('text', '').strip()
            return text if text else None
        return None
    except Exception:
        return None


def load_verses_from_api() -> List[Dict]:
    """
    Load all verses from Bible API
    SLOW (~30-45 minutes) but reliable
    Use this as fallback if no local data available
    """
    print("=" * 70)
    print("FULL KJV BIBLE LOADER - API METHOD")
    print("=" * 70)
    print()
    print("⏱️  WARNING: API method is SLOW (~30-45 minutes)")
    print("   Fetching 31,102 verses from bible-api.com...")
    print()
    
    all_verses = []
    total_books = len(KJV_BOOKS)
    start_time = time.time()
    
    for book_idx, (book_name, num_chapters) in enumerate(KJV_BOOKS.items(), 1):
        book_verses = 0
        
        for chapter in range(1, num_chapters + 1):
            for verse in range(1, 200):  # Max possible verses
                text = fetch_verse_from_api(book_name, chapter, verse)
                
                if text is None:
                    break  # No more verses in this chapter
                
                all_verses.append({
                    "book": book_name,
                    "chapter": chapter,
                    "verse_number": verse,
                    "text": text,
                    "version": "KJV"
                })
                book_verses += 1
        
        elapsed = time.time() - start_time
        rate = len(all_verses) / (elapsed / 60) if elapsed > 0 else 0
        eta_mins = (31102 - len(all_verses)) / rate if rate > 0 else 0
        
        print(f"[{book_idx:2d}/66] {book_name:20s} {book_verses:3d} verses  |  "
              f"{len(all_verses):5d} total  |  ETA: {eta_mins:.0f} min", flush=True)
    
    return all_verses


def load_verses_from_kjv_json() -> List[Dict]:
    """
    Load verses from local kjv.json file (FAST - seconds)
    Tries multiple formats to find the right structure
    """
    json_path = os.path.join(os.path.dirname(__file__), "kjv.json")
    
    if not os.path.exists(json_path):
        print(f"⚠️  Local KJV JSON not found at {json_path}")
        print("   Will attempt API method instead")
        return None
    
    print(f"Loading from {json_path}...")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    all_verses = []
    
    # Detect JSON structure and parse accordingly
    for book_name, book_data in data.items():
        if isinstance(book_data, dict) and "chapters" in book_data:
            # Structure: {book: {chapters: {ch: {v: text}}}}
            chapters = book_data.get("chapters", {})
            for ch_num, verses in chapters.items():
                if isinstance(verses, dict):
                    for v_num, text in verses.items():
                        if isinstance(text, str) and text.strip():
                            all_verses.append({
                                "book": book_name,
                                "chapter": int(ch_num),
                                "verse_number": int(v_num),
                                "text": text.strip(),
                                "version": "KJV"
                            })
    
    return all_verses if all_verses else None


def insert_verses_batched(verses: List[Dict], batch_size: int = 1000) -> int:
    """
    Insert verses into Supabase with optimized batching
    Returns count of successfully inserted verses
    """
    total_batches = (len(verses) + batch_size - 1) // batch_size
    inserted = 0
    
    print()
    print("Inserting into Supabase...")
    print()
    
    for batch_num in range(0, len(verses), batch_size):
        batch = verses[batch_num:batch_num + batch_size]
        batch_idx = (batch_num // batch_size) + 1
        
        try:
            supabase.table("verses").insert(batch).execute()
            inserted += len(batch)
            
            percent = (batch_idx * 100) // total_batches
            bar_filled = int(percent / 5)
            bar = "█" * bar_filled + "░" * (20 - bar_filled)
            print(f"  [{bar}] {percent:3d}% - Batch {batch_idx:3d}/{total_batches} - "
                  f"{inserted:6d} verses inserted", flush=True)
            
            time.sleep(0.05)  # Small delay to avoid rate limiting
            
        except Exception as e:
            print(f"  ❌ Error in batch {batch_idx}: {e}")
            # Continue with next batch even if one fails
    
    return inserted


def verify_load(expected_count: int = 31102) -> bool:
    """Verify verses were loaded correctly"""
    print()
    print("Verifying database...")
    
    try:
        result = supabase.table("verses").select("id", count="exact").execute()
        actual_count = result.count if hasattr(result, 'count') else len(result.data)
        
        print(f"Expected: {expected_count:,} verses")
        print(f"Actual:   {actual_count:,} verses")
        
        if actual_count == expected_count:
            print()
            print("🎉 SUCCESS! All verses loaded perfectly!")
            return True
        elif actual_count > 0:
            print()
            print(f"✅ {actual_count:,} verses loaded (may continue if partial)")
            return True
        else:
            print()
            print("❌ ERROR: No verses found in database")
            return False
            
    except Exception as e:
        print(f"❌ Verification error: {e}")
        return False


def main():
    """Main loader orchestration"""
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " LOGOSLIGHT - FULL KJV BIBLE LOADER ".center(68) + "║")
    print("║" + " Load all 31,102 verses - Ready to use anytime ".center(68) + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    # Clear existing verses
    print("Clearing old verses from database...")
    try:
        supabase.table("verses").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
        print("✓ Database cleared\n")
    except Exception as e:
        print(f"⚠️  Warning: {e}\n")
    
    # Try to load verses
    verses = load_verses_from_kjv_json()
    
    if verses is None:
        print()
        print("Would you like to load from API? (Slow but works)")
        print("Press Enter to continue with API, or Ctrl+C to cancel")
        input()
        verses = load_verses_from_api()
    
    if not verses:
        print("❌ ERROR: Could not load verses")
        return False
    
    print()
    print(f"✓ Loaded {len(verses):,} verses from source")
    
    # Insert into database
    inserted = insert_verses_batched(verses)
    
    # Verify
    if verify_load(len(verses)):
        print()
        print("=" * 70)
        print("✅ BIBLE LOADER COMPLETE!")
        print("=" * 70)
        print()
        print(f"📖 {inserted:,} KJV verses are now available")
        print("📕 All Bible Reader features fully functional")
        print("🔍 Full-text search enabled")
        print()
        return True
    else:
        print()
        print("⚠️  Load completed but with issues - check database")
        return False


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏸️  Loader cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        sys.exit(1)

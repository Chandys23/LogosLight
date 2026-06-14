"""
load_full_kjv.py
Load complete KJV Bible (31,102 verses) into Supabase
Uses bible-api.com with smart batching
"""

import os
import sys
import json
import requests
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from supabase import create_client

load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'backend', '.env'))

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_KEY")
)

# Books of the Bible with chapter counts
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


def fetch_verse(book, chapter, verse):
    """Fetch a single verse using bible-api.com"""
    try:
        # Use text parameter to get just the text
        url = f"https://bible-api.com/{book}%20{chapter}:{verse}?translation=kjv"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            text = data.get('text', '').strip()
            return text if text else None
        return None
    except:
        return None


def load_all_verses():
    """Load all KJV verses from Bible API into Supabase"""
    total_loaded = 0
    batch = []
    batch_size = 100
    books_list = list(BOOKS.items())
    
    print("Clearing old verses...")
    try:
        supabase.table("verses").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
    except:
        pass
    
    print()
    print(f"Fetching {len(books_list)} books from Bible API...")
    print()
    
    for book_idx, (book, chapters) in enumerate(books_list, 1):
        print(f"[{book_idx:2d}/{len(books_list)}] {book:20s}", end=" ", flush=True)
        
        book_verses = 0
        for chapter in range(1, chapters + 1):
            for verse in range(1, 200):  # Max possible verses
                text = fetch_verse(book, chapter, verse)
                
                if text is None:
                    break  # End of verses for this chapter
                
                batch.append({
                    "book": book,
                    "chapter": chapter,
                    "verse_number": verse,
                    "text": text,
                    "version": "KJV"
                })
                book_verses += 1
                total_loaded += 1
                
                # Batch insert when full
                if len(batch) >= batch_size:
                    try:
                        supabase.table("verses").insert(batch).execute()
                    except Exception as e:
                        print(f"\n  Batch error: {e}")
                    batch = []
        
        print(f" {book_verses:4d} verses")
    
    # Final batch
    if batch:
        try:
            supabase.table("verses").insert(batch).execute()
        except Exception as e:
            print(f"Final batch error: {e}")
    
    print()
    print("=" * 70)
    print(f"✓ Loaded {total_loaded} verses!")
    print("=" * 70)


if __name__ == "__main__":
    print("=" * 70)
    print("LogosLight KJV Bible Loader")
    print("=" * 70)
    print()
    
    load_all_verses()

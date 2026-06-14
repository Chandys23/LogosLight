"""
download_full_kjv.py
Download complete KJV Bible from reliable API
"""

import requests
import json
import time

def download_from_api():
    """Download KJV Bible from Bible API"""
    print("Downloading full KJV Bible...")
    
    # These are the 66 books of the Bible with chapter counts
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
    
    bible = {}
    total_verses = 0
    failed_verses = 0
    
    print(f"Fetching {len(BOOKS)} books...\n")
    
    for book_idx, (book_name, num_chapters) in enumerate(BOOKS.items(), 1):
        print(f"[{book_idx:2d}/66] {book_name:20s}", end=" ", flush=True)
        
        bible[book_name] = {
            "name": book_name,
            "chapters": {}
        }
        
        book_verses = 0
        
        for chapter in range(1, num_chapters + 1):
            chapter_verses = {}
            
            for verse in range(1, 200):  # Max verses per chapter
                try:
                    # Use bible-api.com which is free and reliable
                    url = f"https://bible-api.com/{book_name}%20{chapter}:{verse}?translation=kjv"
                    response = requests.get(url, timeout=5)
                    
                    if response.status_code != 200:
                        break  # No more verses in this chapter
                    
                    data = response.json()
                    text = data.get('text', '').strip()
                    
                    if text:
                        chapter_verses[verse] = text
                        book_verses += 1
                        total_verses += 1
                    else:
                        break
                        
                except Exception as e:
                    failed_verses += 1
                    break  # Stop trying this chapter
            
            if chapter_verses:
                bible[book_name]["chapters"][str(chapter)] = chapter_verses
        
        print(f"✓ ({book_verses:3d} verses)")
        time.sleep(0.05)  # Rate limiting
    
    print(f"\n✓ Downloaded {total_verses:,} verses ({failed_verses} failures)")
    
    # Save to file
    with open("bible-kjv-full.json", "w", encoding="utf-8") as f:
        json.dump(bible, f, ensure_ascii=False, indent=None)
    
    print(f"✓ Saved to bible-kjv-full.json")
    
    return total_verses


if __name__ == "__main__":
    try:
        total = download_from_api()
        print(f"\n🎉 Ready to load {total:,} verses into database!")
    except Exception as e:
        print(f"ERROR: {e}")

"""
database.py — Supabase verse lookups
"""

import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_KEY")
)


def get_random_verse() -> dict | None:
    """Get a random verse by fetching all and picking one randomly in Python."""
    try:
        import random
        response = supabase.table("verses").select("book,chapter,verse_number,text").execute()
        if response.data:
            verse = random.choice(response.data)
            return {
                "book": verse["book"],
                "chapter": verse["chapter"],
                "verse_number": verse["verse_number"],
                "text": verse["text"],
                "reference": f"{verse['book']} {verse['chapter']}:{verse['verse_number']}"
            }
        return None
    except Exception as e:
        print(f"Error fetching random verse: {e}")
        return None


def get_verses_by_references(references: list[str]) -> list[dict]:
    """
    Fetch verse texts from Supabase for a list of reference strings.

    Args:
        references: e.g. ["Philippians 4:6", "Matthew 6:34"]

    Returns:
        List of verse dicts with keys: book, chapter, verse_number, text, reference
    """
    verses = []
    for ref in references:
        try:
            # Split "1 Corinthians 13:4" -> book="1 Corinthians", rest="13:4"
            book, rest = ref.rsplit(" ", 1)
            chapter, verse_num = rest.split(":")
            response = (
                supabase.table("verses")
                .select("book, chapter, verse_number, text")
                .eq("book", book.strip())
                .eq("chapter", int(chapter))
                .eq("verse_number", int(verse_num))
                .execute()
            )
            if response.data:
                v = response.data[0]
                verses.append({
                    "book": v["book"],
                    "chapter": v["chapter"],
                    "verse_number": v["verse_number"],
                    "text": v["text"],
                    "reference": f"{v['book']} {v['chapter']}:{v['verse_number']}"
                })
        except Exception as e:
            print(f"Error parsing reference {ref}: {e}")
            continue
    return verses


def search_verses(query: str, limit: int = 10) -> list[dict]:
    """Search verses by text (case-insensitive substring match)."""
    try:
        response = (
            supabase.table("verses")
            .select("book, chapter, verse_number, text")
            .ilike("text", f"%{query}%")
            .limit(limit)
            .execute()
        )
        return [
            {
                "book": v["book"],
                "chapter": v["chapter"],
                "verse_number": v["verse_number"],
                "text": v["text"],
                "reference": f"{v['book']} {v['chapter']}:{v['verse_number']}"
            }
            for v in response.data
        ]
    except Exception as e:
        print(f"Error searching verses: {e}")
        return []


# Bible Reader Functions

def get_all_books() -> list[dict]:
    """Get unique list of all books with verse count."""
    try:
        response = (
            supabase.table("verses")
            .select("book")
            .execute()
        )
        
        books_dict = {}
        for row in response.data:
            book = row["book"]
            if book not in books_dict:
                books_dict[book] = 0
            books_dict[book] += 1
        
        return [
            {"book": book, "verse_count": count}
            for book, count in books_dict.items()
        ]
    except Exception as e:
        print(f"Error fetching books: {e}")
        return []


def get_chapters_in_book(book: str) -> list[int]:
    """Get all chapter numbers for a book."""
    try:
        response = (
            supabase.table("verses")
            .select("chapter")
            .eq("book", book)
            .order("chapter")
            .execute()
        )
        
        chapters = sorted(list(set([r["chapter"] for r in response.data])))
        return chapters
    except Exception as e:
        print(f"Error fetching chapters for {book}: {e}")
        return []


def get_verses_in_chapter(book: str, chapter: int) -> list[dict]:
    """Get all verses in a specific chapter."""
    try:
        response = (
            supabase.table("verses")
            .select("book, chapter, verse_number, text")
            .eq("book", book)
            .eq("chapter", chapter)
            .order("verse_number")
            .execute()
        )
        
        return [
            {
                "book": v["book"],
                "chapter": v["chapter"],
                "verse_number": v["verse_number"],
                "text": v["text"]
            }
            for v in response.data
        ]
    except Exception as e:
        print(f"Error fetching verses for {book} {chapter}: {e}")
        return []


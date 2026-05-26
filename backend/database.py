import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)


def get_random_verse() -> dict | None:
    """Get a random verse using a server-side SQL RANDOM() call — does NOT load all rows."""
    response = supabase.rpc("get_random_verse").execute()
    return response.data[0] if response.data else None


def get_verses_by_references(references: list[str]) -> list[dict]:
    """
    Fetch verse texts from Supabase for a list of reference strings.

    Args:
        references: e.g. ["Philippians 4:6", "Matthew 6:34"]

    Returns:
        List of verse dicts with keys: book, chapter, verse_number, text
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
                verses.append(response.data[0])
        except Exception:
            continue
    return verses

import os
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from database import get_random_verse, get_verses_by_references, get_all_books, get_chapters_in_book, get_verses_in_chapter, search_verses
from claude import get_verse_references, generate_emotion_devotional, generate_deep_study

load_dotenv()

app = FastAPI(
    title="LogosLight API",
    version="2.0.0",
    description="Christian devotional app — KJV scripture + Claude AI",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        os.getenv("FRONTEND_URL", "https://logos-light.vercel.app"),
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class EmotionRequest(BaseModel):
    emotion: str


class StudyRequest(BaseModel):
    topic: str


@app.get("/api/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.get("/api/verses/verse-of-day")
def verse_of_day():
    verse = get_random_verse()
    if not verse:
        raise HTTPException(status_code=500, detail="Could not retrieve verse")
    return {
        "reference": f"{verse['book']} {verse['chapter']}:{verse['verse_number']}",
        "text": verse["text"],
        "book": verse["book"],
        "chapter": verse["chapter"],
        "verse": verse["verse_number"],
    }


@app.post("/api/devotional/emotion")
def emotion_devotional(request: EmotionRequest):
    emotion = request.emotion.strip() if request.emotion else ""
    if len(emotion) < 2:
        raise HTTPException(status_code=400, detail="Please describe your emotion")

    refs = get_verse_references(emotion)
    verses = get_verses_by_references(refs)
    if not verses:
        raise HTTPException(status_code=500, detail="Could not load verses")

    result = generate_emotion_devotional(emotion, verses)

    return {
        "emotion": emotion,
        "verses": [{"reference": f"{v['book']} {v['chapter']}:{v['verse_number']}", "text": v["text"]} for v in verses],
        "prayer": result["prayer"],
        "encouragement": result["encouragement"],
        "full_response": result["response"],
    }


@app.post("/api/ai-study/search")
def ai_deep_study(request: StudyRequest):
    topic = request.topic.strip() if request.topic else ""
    if len(topic) < 2:
        raise HTTPException(status_code=400, detail="Please provide a topic")

    refs = get_verse_references(topic)
    verses = get_verses_by_references(refs)
    if not verses:
        raise HTTPException(status_code=500, detail="Could not load verses")

    result = generate_deep_study(topic, verses)

    return {
        "topic": topic,
        "verses": [{"reference": f"{v['book']} {v['chapter']}:{v['verse_number']}", "text": v["text"]} for v in verses],
        "study_guide": result["response"],
    }


# Bible Reader Endpoints

@app.get("/api/bible/books")
def get_bible_books():
    """Get list of all books in the KJV Bible."""
    books = get_all_books()
    if not books:
        raise HTTPException(status_code=500, detail="Could not load Bible books")
    return {
        "total_books": len(books),
        "books": books
    }


@app.get("/api/bible/{book}/chapters")
def get_book_chapters(book: str):
    """Get all chapter numbers for a book."""
    chapters = get_chapters_in_book(book)
    if not chapters:
        raise HTTPException(status_code=404, detail=f"Book '{book}' not found")
    
    return {
        "book": book,
        "total_chapters": len(chapters),
        "chapters": chapters
    }


@app.get("/api/bible/{book}/{chapter}")
def get_chapter_verses(book: str, chapter: int):
    """Get all verses in a chapter."""
    verses = get_verses_in_chapter(book, chapter)
    if not verses:
        raise HTTPException(
            status_code=404, 
            detail=f"{book} {chapter} not found"
        )
    
    return {
        "reference": f"{book} {chapter}",
        "total_verses": len(verses),
        "verses": [
            {
                "verse": v['verse_number'],
                "text": v['text']
            }
            for v in verses
        ]
    }


@app.get("/api/bible/search")
def search_bible(q: str = None):
    """Full-text search the Bible."""
    if not q or len(q.strip()) < 2:
        raise HTTPException(status_code=400, detail="Search query too short (min 2 characters)")
    
    verses = search_verses(q.strip(), limit=50)
    return {
        "query": q,
        "results_count": len(verses),
        "verses": [
            {
                "reference": f"{v['book']} {v['chapter']}:{v['verse_number']}",
                "text": v['text']
            }
            for v in verses
        ]
    }

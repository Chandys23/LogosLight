import os
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from database import get_random_verse, get_verses_by_references
from claude import get_verse_references, generate_emotion_devotional, generate_deep_study

load_dotenv()

app = FastAPI(
    title="LogosLight API",
    version="2.0.0",
    description="Christian devotional app — KJV scripture + Claude Haiku",
)

# ---------------------------------------------------------------------------
# CORS — allow local dev and production Vercel URL
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------

class EmotionRequest(BaseModel):
    emotion: str  # Free text — no hardcoded validation; Claude handles anything


class StudyRequest(BaseModel):
    topic: str


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.get("/api/verses/verse-of-day")
def verse_of_day():
    """Return one random KJV verse using SQL RANDOM() LIMIT 1."""
    verse = get_random_verse()
    if not verse:
        raise HTTPException(status_code=500, detail="Could not retrieve verse of the day")
    return {
        "reference": f"{verse['book']} {verse['chapter']}:{verse['verse_number']}",
        "text": verse["text"],
        "book": verse["book"],
        "chapter": verse["chapter"],
        "verse": verse["verse_number"],
        "reflection": "Meditate on this verse and how God is speaking to you today.",
        "apply_today": "Find one practical way to live out this scripture today.",
    }


@app.post("/api/devotional/emotion")
def emotion_devotional(request: EmotionRequest):
    """
    Accept any emotion or feeling as free text.
    No hardcoded list — Claude handles any input.
    """
    emotion = request.emotion.strip() if request.emotion else ""
    if len(emotion) < 2:
        raise HTTPException(status_code=400, detail="Please describe your emotion or feeling")

    refs = get_verse_references(emotion)
    verses = get_verses_by_references(refs)
    if not verses:
        raise HTTPException(status_code=500, detail="Could not load scripture. Please try again.")

    result = generate_emotion_devotional(emotion, verses)

    return {
        "emotion": emotion,
        "verses": [
            {
                "reference": f"{v['book']} {v['chapter']}:{v['verse_number']}",
                "text": v["text"],
            }
            for v in verses
        ],
        "prayer": result["prayer"],
        "encouragement": result["encouragement"],
        "full_response": result["response"],
    }


@app.post("/api/ai-study/search")
def ai_deep_study(request: StudyRequest):
    """
    Generate a deep study guide for any topic, question, or scripture theme.
    Useful for sermon prep, worship planning, or personal study.
    """
    topic = request.topic.strip() if request.topic else ""
    if len(topic) < 2:
        raise HTTPException(status_code=400, detail="Please provide a study topic or question")

    refs = get_verse_references(topic)
    verses = get_verses_by_references(refs)
    if not verses:
        raise HTTPException(status_code=500, detail="Could not load scripture. Please try again.")

    result = generate_deep_study(topic, verses)

    return {
        "topic": topic,
        "verses": [
            {
                "reference": f"{v['book']} {v['chapter']}:{v['verse_number']}",
                "text": v["text"],
            }
            for v in verses
        ],
        "study_guide": result["response"],
    }

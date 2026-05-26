# LogosLight - Complete Implementation Guide

**Version:** 2.0 MVP (Simplified Stack)  
**Last Updated:** May 25, 2026  
**Status:** Ready for Development  

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Tech Stack](#tech-stack)
3. [Project Structure](#project-structure)
4. [Step-by-Step Implementation](#step-by-step-implementation)
5. [Database Schema](#database-schema)
6. [API Specifications](#api-specifications)
7. [Frontend Implementation](#frontend-implementation)
8. [Deployment Guide](#deployment-guide)
9. [Testing Strategy](#testing-strategy)
10. [Timeline & Milestones](#timeline--milestones)

---

## Architecture Overview

### High-Level Architecture Diagram

```
+------------------------------------------------------------------+
|                         User Browser                              |
|                                                                    |
|  +--------------------------------------------------------------+ |
|  |              React SPA (Vercel)                               | |
|  |  - Home (Verse of the Day Banner)                             | |
|  |  - Emotion-Based Devotional (open input)                      | |
|  |  - AI Deep Study Guide                                        | |
|  +--------------------------------------------------------------+ |
+------------------------------------------------------------------+
                            |
                            | HTTPS Requests
                            v
+------------------------------------------------------------------+
|                  FastAPI Backend (Render.com)                     |
|                                                                    |
|  +-----------------------------------------------------------+    |
|  |           3-File Backend (main, database, claude)          |    |
|  |  - GET  /api/verses/verse-of-day                          |    |
|  |  - POST /api/devotional/emotion                           |    |
|  |  - POST /api/ai-study/search                              |    |
|  |  - GET  /api/health                                       |    |
|  +-----------------------------------------------------------+    |
|                     |                    |                         |
|                     v                    v                         |
|            Supabase DB          Anthropic Claude Haiku            |
|          (simple lookup)         (text generation)                |
+------------------------------------------------------------------+
                    |
        +-----------+-----------+
        v                       v
   +-------------+      +--------------+
   | Supabase    |      | Anthropic    |
   | PostgreSQL  |      | Claude Haiku |
   |             |      | API          |
   | - verses    |      |              |
   |   (standard |      | - Devotional |
   |   SQL table)|      | - Deep Study |
   +-------------+      +--------------+
```

### Simplified Data Flow

```
User Opens App
    |
    v
React loads from Vercel
    |
    v
User selects feature
    |
    v
Frontend calls FastAPI endpoint
    |

-- VERSE OF DAY --------------------------------------------------
SELECT * FROM verses ORDER BY RANDOM() LIMIT 1
Return verse to frontend

-- EMOTION DEVOTIONAL --------------------------------------------
1. Look up verse references from VERSE_MAP[emotion]
   (or use open text input directly)
2. Fetch those verse texts from Supabase by reference
3. Build prompt with KJV verses + user emotion
4. Call Claude Haiku => get prayer, encouragement, explanation
5. Return to frontend

-- AI DEEP STUDY ------------------------------------------------
1. Look up verse references from STUDY_MAP[topic]
   (or use open text input directly)
2. Fetch those verse texts from Supabase
3. Build prompt with KJV verses + topic
4. Call Claude Haiku => get study guide, sermon notes, application
5. Return to frontend
```

---

## Bible Version & Licensing Decision

### KJV (King James Version) - Public Domain PERMANENT CHOICE

| Aspect | Details |
|--------|---------|
| **Version** | KJV (King James Version, 1611) |
| **Legal Status** | Public domain - zero copyright concerns |
| **Cost** | $0 forever |
| **Source** | GitHub: scrollmapper/bible_databases |
| **Total Verses** | 31,102 (OT: 23,145 / NT: 7,957) |
| **Migration** | None planned - KJV is the permanent choice |

---

## Tech Stack

### Frontend
| Component | Technology | Why |
|-----------|-----------|-----|
| Framework | React 18 + Vite | Fast, modern, simple |
| Styling | Tailwind CSS | Utility-first, spiritual color palette |
| HTTP Client | Axios | Simple API calls |
| State | useState | Sufficient for MVP |
| Hosting | Vercel | Free, auto-deploys from GitHub |

### Backend (3 files)
| Component | Technology | Why |
|-----------|-----------|-----|
| Framework | FastAPI | Fast, async, auto-generates API docs |
| Language | Python 3.11+ | Clean, readable |
| Server | Uvicorn | ASGI, handles async |
| DB Client | Supabase SDK | Simple .select() / .eq() calls |
| LLM | Anthropic Claude Haiku | Reliable, high quality, ~$1-5/month |
| Hosting | Render.com | Free tier, auto-deploys from GitHub |

### Database (No Vector Search)
| Component | Technology | Why |
|-----------|-----------|-----|
| Database | Supabase (PostgreSQL) | Managed, free tier (500MB) |
| Lookup | Standard SQL | Simple reference-based queries, no pgvector needed |

### AI
| Component | Technology | Why |
|-----------|-----------|-----|
| LLM | Claude Haiku (Anthropic) | Reliable, fast, compassionate output |
| Verse Selection | Curated VERSE_MAP | Zero infra, deterministic, easy to extend |

### External Services
| Service | Provider | Cost |
|---------|----------|------|
| Frontend Hosting | Vercel | FREE |
| Backend Hosting | Render.com | FREE |
| Database | Supabase | FREE (500MB) |
| Bible Data | GitHub (KJV) | FREE |
| LLM Inference | Anthropic Claude Haiku | ~$1-5/month |
| **Total Monthly Cost** | | **~$1-5** |

---

## Project Structure

### Simplified 3-File Backend

```
logos-light/
|
+-- backend/
|   +-- main.py          # FastAPI app + ALL routes
|   +-- database.py      # Supabase connection + verse lookups
|   +-- claude.py        # Claude API calls + all prompts + verse map
|   +-- requirements.txt
|   +-- Procfile         # Render deployment
|   +-- .env
|   +-- .env.example
|
+-- frontend/
|   +-- src/
|   |   +-- components/
|   |   |   +-- VerseOfDay.jsx
|   |   |   +-- EmotionBasedDevotional.jsx
|   |   |   +-- AIDeepStudyGuide.jsx
|   |   |   +-- Navigation.jsx
|   |   |   +-- LoadingSpinner.jsx
|   |   |
|   |   +-- pages/
|   |   |   +-- Home.jsx
|   |   |   +-- EmotionBasedDevotionalPage.jsx
|   |   |   +-- AIDeepStudyGuidePage.jsx
|   |   |
|   |   +-- utils/
|   |   |   +-- api.js       # Axios API client
|   |   |
|   |   +-- App.jsx
|   |   +-- main.jsx
|   |
|   +-- package.json
|   +-- vite.config.js
|   +-- tailwind.config.js
|   +-- .env
|
+-- scripts/
|   +-- download_bible.py   # Download KJV JSON
|   +-- load_verses.py      # Load 31K verses into Supabase
|
+-- README.md
```

---

## Step-by-Step Implementation

### Phase 1: Backend Setup (Days 1-3)

#### Step 1.1: Initialize Project

```bash
mkdir logos-light-backend
cd logos-light-backend

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# Create the 3 main files
New-Item main.py, database.py, claude.py, requirements.txt
```

#### Step 1.2: requirements.txt

```
fastapi==0.104.0
uvicorn[standard]==0.24.0
python-dotenv==1.0.0
supabase==2.0.0
anthropic==0.25.0
pydantic==2.4.0
httpx==0.25.2
pytest==7.4.3
```

```bash
pip install -r requirements.txt
```

#### Step 1.3: .env File

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key
ANTHROPIC_API_KEY=sk-ant-your-key-here
DEBUG=True
```

---

#### Step 1.4: database.py - Supabase Connection & Lookups

```python
# database.py
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def get_random_verse():
    """Get a random verse using SQL RANDOM() - no memory load."""
    response = supabase.rpc('get_random_verse').execute()
    return response.data[0] if response.data else None

def get_verses_by_references(references: list[str]) -> list[dict]:
    """
    Fetch verse texts for a list of references.
    references = ["Philippians 4:6", "Matthew 6:34", ...]
    """
    verses = []
    for ref in references:
        try:
            book, rest = ref.rsplit(' ', 1)
            chapter, verse_num = rest.split(':')
            response = supabase.table('verses') \
                .select('book, chapter, verse_number, text') \
                .eq('book', book.strip()) \
                .eq('chapter', int(chapter)) \
                .eq('verse_number', int(verse_num)) \
                .execute()
            if response.data:
                verses.append(response.data[0])
        except Exception:
            continue
    return verses
```

---

#### Step 1.5: claude.py - Claude API + Verse Map + Prompts

```python
# claude.py
import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
CLAUDE_MODEL = "claude-haiku-4-5"

# Curated Verse Map
# Each emotion/topic maps to hand-picked KJV references.
# Add more entries as the app grows.

VERSE_MAP = {
    # Emotions
    "anxious":     ["Philippians 4:6", "Matthew 6:34", "1 Peter 5:7", "Isaiah 41:10"],
    "sad":         ["Psalm 34:18", "John 11:35", "Matthew 5:4", "Psalm 147:3"],
    "lost":        ["Proverbs 3:5", "John 14:6", "Psalm 119:105", "Jeremiah 29:11"],
    "grateful":    ["1 Thessalonians 5:18", "Psalm 107:1", "Colossians 3:17"],
    "seeking":     ["Matthew 7:7", "Jeremiah 29:13", "Proverbs 8:17", "Psalm 27:4"],
    "joyful":      ["Philippians 4:4", "Psalm 118:24", "John 15:11", "Romans 15:13"],
    "overwhelmed": ["Matthew 11:28", "Isaiah 40:31", "Psalm 61:2", "2 Corinthians 4:8"],
    "lonely":      ["Hebrews 13:5", "Psalm 68:6", "Isaiah 43:2", "Matthew 28:20"],
    "hopeful":     ["Romans 15:13", "Jeremiah 29:11", "Psalm 31:24", "Hebrews 11:1"],
    # Deep Study Topics
    "faith":       ["Hebrews 11:1", "Romans 10:17", "James 2:17", "Matthew 17:20"],
    "prayer":      ["Matthew 6:9", "1 Thessalonians 5:17", "Philippians 4:6", "James 5:16"],
    "love":        ["1 Corinthians 13:4", "John 3:16", "1 John 4:8", "Romans 8:38"],
    "grace":       ["Ephesians 2:8", "2 Corinthians 12:9", "Romans 5:8", "Titus 2:11"],
    "forgiveness": ["Ephesians 4:32", "Matthew 6:14", "Colossians 3:13", "1 John 1:9"],
    "strength":    ["Isaiah 40:31", "Philippians 4:13", "Psalm 46:1", "2 Corinthians 12:10"],
    "wisdom":      ["Proverbs 3:5", "James 1:5", "Proverbs 9:10", "Colossians 2:3"],
    "salvation":   ["John 3:16", "Romans 10:9", "Acts 4:12", "Ephesians 2:8"],
}

def get_verse_references(query: str) -> list[str]:
    """
    Return curated verse references for a query.
    Falls back to general comfort verses if no match found.
    Claude handles the interpretation - any input works.
    """
    query_lower = query.lower().strip()
    if query_lower in VERSE_MAP:
        return VERSE_MAP[query_lower]
    for key in VERSE_MAP:
        if key in query_lower or query_lower in key:
            return VERSE_MAP[key]
    # Default: general comfort verses for unknown input
    return [
        "Psalm 23:1", "John 3:16", "Romans 8:28",
        "Philippians 4:13", "Isaiah 40:31"
    ]

# Prompts

EMOTION_PROMPT = """\
You are a compassionate Christian spiritual guide. The user is feeling: {emotion}

Here are relevant KJV Bible verses:
{verses}

Respond with:
1. A brief explanation of how each verse speaks to their feeling (2-3 sentences each)
2. A short prayer based on these scriptures (3-4 sentences, start with "Heavenly Father,")
3. An encouragement message grounded in the verses (2-3 sentences)

Format your response with clear section headers: Verse Reflections, Prayer, Encouragement.
Keep your tone warm, compassionate, and strictly grounded in the provided scriptures."""

AI_DEEP_STUDY_PROMPT = """\
You are a Biblical scholar and pastor. The study topic or question is: {topic}

Here are key KJV Bible verses on this topic:
{verses}

Respond with:
1. An overview of this topic from scripture (3-4 sentences)
2. Verse-by-verse explanation and connection to the topic (2-3 sentences each)
3. Practical application for daily Christian life or sermon use (3-4 sentences)
4. A suggested reflection question for personal study or congregation discussion

Format with clear headers: Overview, Verse Explanations, Application, Reflection Question.
Ground your response strictly in the provided scriptures."""

# Claude API Calls

def call_claude(prompt: str) -> str:
    """Call Claude Haiku and return text response."""
    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

def generate_emotion_devotional(emotion: str, verses: list[dict]) -> dict:
    """Generate devotional content for a given emotion + verse list."""
    verses_text = "\n".join([
        f"- {v['book']} {v['chapter']}:{v['verse_number']}: \"{v['text']}\""
        for v in verses
    ])
    prompt = EMOTION_PROMPT.format(emotion=emotion, verses=verses_text)
    response = call_claude(prompt)

    prayer = ""
    encouragement = ""
    if "Prayer" in response:
        parts = response.split("Prayer")
        prayer = parts[1].split("\n\n")[0].replace(":", "").strip()
    if "Encouragement" in response:
        parts = response.split("Encouragement")
        encouragement = parts[1].split("\n\n")[0].replace(":", "").strip()

    return {
        "response": response,
        "prayer": prayer or "Father, guide us by Your word. Amen.",
        "encouragement": encouragement or "Trust in God's unfailing love."
    }

def generate_deep_study(topic: str, verses: list[dict]) -> dict:
    """Generate AI deep study content for a topic + verse list."""
    verses_text = "\n".join([
        f"- {v['book']} {v['chapter']}:{v['verse_number']}: \"{v['text']}\""
        for v in verses
    ])
    prompt = AI_DEEP_STUDY_PROMPT.format(topic=topic, verses=verses_text)
    response = call_claude(prompt)
    return {"response": response}
```

---

#### Step 1.6: main.py - FastAPI App + All Routes

```python
# main.py
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from dotenv import load_dotenv

from database import get_random_verse, get_verses_by_references
from claude import get_verse_references, generate_emotion_devotional, generate_deep_study

load_dotenv()

app = FastAPI(
    title="LogosLight API",
    version="2.0.0",
    description="Christian devotional app powered by KJV scripture and Claude Haiku"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://logos-light.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Models

class EmotionRequest(BaseModel):
    emotion: str  # Any free text - no hardcoded validation

class StudyRequest(BaseModel):
    topic: str

# Routes

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/api/verses/verse-of-day")
def verse_of_day():
    """Returns one random verse using SQL RANDOM() LIMIT 1."""
    verse = get_random_verse()
    if not verse:
        raise HTTPException(status_code=500, detail="No verses found")
    return {
        "reference": f"{verse['book']} {verse['chapter']}:{verse['verse_number']}",
        "text": verse["text"],
        "book": verse["book"],
        "chapter": verse["chapter"],
        "verse": verse["verse_number"],
        "reflection": "Meditate on this verse and how God is speaking to you today.",
        "apply_today": "Find one practical way to live out this scripture today."
    }

@app.post("/api/devotional/emotion")
def emotion_devotional(request: EmotionRequest):
    """
    Accept ANY emotion string (open input).
    No hardcoded validation - Claude handles anything.
    """
    if not request.emotion or len(request.emotion.strip()) < 2:
        raise HTTPException(status_code=400, detail="Please describe your emotion")

    emotion = request.emotion.strip()
    refs = get_verse_references(emotion)
    verses = get_verses_by_references(refs)
    if not verses:
        raise HTTPException(status_code=500, detail="Could not load verses")

    result = generate_emotion_devotional(emotion, verses)

    return {
        "emotion": emotion,
        "verses": [
            {
                "reference": f"{v['book']} {v['chapter']}:{v['verse_number']}",
                "text": v["text"]
            }
            for v in verses
        ],
        "prayer": result["prayer"],
        "encouragement": result["encouragement"],
        "full_response": result["response"]
    }

@app.post("/api/ai-study/search")
def ai_deep_study(request: StudyRequest):
    """
    Deep study for any topic - sermon prep, scripture deep-dive,
    character study, worship planning, or theological question.
    """
    if not request.topic or len(request.topic.strip()) < 2:
        raise HTTPException(status_code=400, detail="Please provide a study topic")

    topic = request.topic.strip()
    refs = get_verse_references(topic)
    verses = get_verses_by_references(refs)
    if not verses:
        raise HTTPException(status_code=500, detail="Could not load verses")

    result = generate_deep_study(topic, verses)

    return {
        "topic": topic,
        "verses": [
            {
                "reference": f"{v['book']} {v['chapter']}:{v['verse_number']}",
                "text": v["text"]
            }
            for v in verses
        ],
        "study_guide": result["response"]
    }
```

---

### Phase 2: Database Setup (Days 3-4)

#### Step 2.1: Create verses Table in Supabase

```sql
-- Run in Supabase SQL Editor

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

-- Index for reference-based lookups
CREATE INDEX idx_verses_ref ON verses(book, chapter, verse_number);
```

No VECTOR column. No pgvector extension. Standard SQL only.

#### Step 2.2: Create the SQL function for RANDOM() verse

```sql
-- Supabase SQL Editor
CREATE OR REPLACE FUNCTION get_random_verse()
RETURNS TABLE(book VARCHAR, chapter INT, verse_number INT, text TEXT)
LANGUAGE sql
AS $$
    SELECT book, chapter, verse_number, text
    FROM verses
    ORDER BY RANDOM()
    LIMIT 1;
$$;
```

This fetches exactly 1 verse - it does NOT load all 31,102 rows into memory.

#### Step 2.3: Download KJV Bible Data

```python
# scripts/download_bible.py
import requests, json

url = "https://raw.githubusercontent.com/scrollmapper/bible_databases/master/json/bible-en-kjv.json"
print("Downloading KJV Bible...")
r = requests.get(url)
r.raise_for_status()
with open("scripts/bible-kjv.json", "w") as f:
    json.dump(r.json(), f)
print("Done - bible-kjv.json saved")
```

#### Step 2.4: Load All 31,102 Verses into Supabase

```python
# scripts/load_verses.py
import json, os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def load():
    print("LogosLight KJV Loader\n")
    with open("scripts/bible-kjv.json", encoding="utf-8") as f:
        data = json.load(f)

    verses, total_books = [], len(data)
    for i, book in enumerate(data, 1):
        print(f"  [{i}/{total_books}] {book['name']}")
        for ch_num, chapter in enumerate(book["chapters"], 1):
            for v_num, text in enumerate(chapter, 1):
                if text.strip():
                    verses.append({
                        "book": book["name"],
                        "chapter": ch_num,
                        "verse_number": v_num,
                        "text": text,
                        "version": "KJV"
                    })

    print(f"\nParsed {len(verses):,} verses")

    batch_size = 1000
    batches = (len(verses) + batch_size - 1) // batch_size
    for n, i in enumerate(range(0, len(verses), batch_size), 1):
        supabase.table("verses").insert(verses[i:i+batch_size]).execute()
        print(f"  Batch {n}/{batches} done")
        time.sleep(0.3)

    count = supabase.table("verses").select("id", count="exact").execute().count
    print(f"\nDatabase has {count:,} verses")
    if count == 31102:
        print("All 31,102 verses loaded successfully!")

if __name__ == "__main__":
    load()
```

```bash
python scripts/load_verses.py
```

---

### Phase 3: Frontend Setup (Days 5-8)

#### Step 3.1: Create React Project

```bash
npm create vite@latest logos-light-frontend -- --template react
cd logos-light-frontend
npm install
npm install axios tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

#### Step 3.2: Configure Tailwind

```javascript
// tailwind.config.js
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        'divine-gold':   '#D4AF37',
        'faith-blue':    '#1B3A57',
        'spirit-cream':  '#F5E6D3',
        'life-green':    '#7CB342',
        'spirit-purple': '#9575CD',
      },
      fontFamily: {
        scripture: ['Georgia', 'serif'],
        body:      ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
```

#### Step 3.3: API Client

```javascript
// src/utils/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: { 'Content-Type': 'application/json' },
});

export const verseService = {
  getVerseOfDay: () => api.get('/api/verses/verse-of-day'),
};

export const devotionalService = {
  getDevotional: (emotion) =>
    api.post('/api/devotional/emotion', { emotion }),
};

export const studyService = {
  getStudyGuide: (topic) =>
    api.post('/api/ai-study/search', { topic }),
};

export default api;
```

#### Step 3.4: VerseOfDay Component (Home Page Banner)

```jsx
// src/components/VerseOfDay.jsx
import React, { useEffect, useState } from 'react';
import { verseService } from '../utils/api';

export default function VerseOfDay() {
  const [verse, setVerse] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    verseService.getVerseOfDay()
      .then(r => setVerse(r.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return (
    <div className="flex justify-center py-20">
      <div className="animate-spin h-10 w-10 rounded-full border-b-2 border-divine-gold" />
    </div>
  );

  return (
    <div className="bg-gradient-to-br from-faith-blue to-divine-gold text-white rounded-xl shadow-xl p-10 my-8 text-center">
      <p className="text-xs tracking-widest uppercase opacity-75 mb-4">Verse of the Day</p>
      <blockquote className="font-scripture text-2xl md:text-3xl leading-relaxed italic mb-6">
        "{verse?.text}"
      </blockquote>
      <p className="font-semibold text-divine-gold text-lg">{verse?.reference}</p>
      <div className="mt-6 grid md:grid-cols-2 gap-4 text-left">
        <div className="bg-white bg-opacity-10 rounded-lg p-4">
          <p className="font-semibold mb-1">Reflection</p>
          <p className="text-sm opacity-90">{verse?.reflection}</p>
        </div>
        <div className="bg-white bg-opacity-10 rounded-lg p-4">
          <p className="font-semibold mb-1">Apply Today</p>
          <p className="text-sm opacity-90">{verse?.apply_today}</p>
        </div>
      </div>
    </div>
  );
}
```

#### Step 3.5: EmotionBasedDevotional Component

```jsx
// src/components/EmotionBasedDevotional.jsx
import React, { useState } from 'react';
import { devotionalService } from '../utils/api';

const PRESET_EMOTIONS = [
  'Anxious', 'Sad', 'Lost', 'Grateful', 'Seeking',
  'Joyful', 'Overwhelmed', 'Lonely', 'Hopeful'
];

export default function EmotionBasedDevotional() {
  const [emotion, setEmotion]   = useState('');
  const [result, setResult]     = useState(null);
  const [loading, setLoading]   = useState(false);
  const [error, setError]       = useState(null);

  const handleSubmit = async () => {
    if (!emotion.trim()) return;
    setLoading(true); setError(null); setResult(null);
    try {
      const r = await devotionalService.getDevotional(emotion);
      setResult(r.data);
    } catch (e) {
      setError(e.response?.data?.detail || 'Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto py-8">
      <h2 className="text-3xl font-bold text-faith-blue text-center mb-8">
        How Are You Feeling?
      </h2>

      <div className="grid grid-cols-3 md:grid-cols-5 gap-3 mb-6">
        {PRESET_EMOTIONS.map(e => (
          <button key={e}
            onClick={() => setEmotion(e)}
            className={`py-3 rounded-lg font-medium transition text-sm ${
              emotion === e
                ? 'bg-divine-gold text-white shadow-md'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >{e}</button>
        ))}
      </div>

      <textarea
        value={emotion}
        onChange={e => setEmotion(e.target.value)}
        placeholder="Or describe how you're feeling in your own words..."
        rows={3}
        className="w-full border border-gray-300 rounded-lg p-4 text-gray-700 focus:outline-none focus:border-faith-blue mb-4 resize-none"
      />

      <button
        onClick={handleSubmit}
        disabled={loading || !emotion.trim()}
        className="w-full bg-faith-blue text-white py-4 rounded-lg font-semibold text-lg hover:bg-opacity-90 disabled:opacity-50 transition"
      >
        {loading ? 'Finding scripture for you...' : 'Get Devotional'}
      </button>

      {error && (
        <div className="mt-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      {result && (
        <div className="mt-8 space-y-6">
          <div>
            <h3 className="text-xl font-bold text-faith-blue mb-4">Relevant Verses</h3>
            {result.verses.map((v, i) => (
              <div key={i} className="bg-spirit-cream border-l-4 border-divine-gold p-5 rounded-lg mb-4">
                <p className="font-semibold text-faith-blue mb-2">{v.reference}</p>
                <p className="font-scripture italic text-gray-800">"{v.text}"</p>
              </div>
            ))}
          </div>

          <div className="bg-green-50 border-l-4 border-life-green p-6 rounded-lg">
            <h3 className="font-bold text-faith-blue mb-3">Prayer</h3>
            <p className="text-gray-700 leading-relaxed whitespace-pre-line">{result.prayer}</p>
          </div>

          <div className="bg-purple-50 border-l-4 border-spirit-purple p-6 rounded-lg">
            <h3 className="font-bold text-faith-blue mb-3">Encouragement</h3>
            <p className="text-gray-700 leading-relaxed whitespace-pre-line">{result.encouragement}</p>
          </div>
        </div>
      )}
    </div>
  );
}
```

#### Step 3.6: AIDeepStudyGuide Component

```jsx
// src/components/AIDeepStudyGuide.jsx
import React, { useState } from 'react';
import { studyService } from '../utils/api';

const STUDY_SUGGESTIONS = [
  'Faith', 'Prayer', 'Love', 'Grace', 'Forgiveness',
  'Salvation', 'Wisdom', 'Strength', 'The Holy Spirit'
];

export default function AIDeepStudyGuide() {
  const [topic, setTopic]     = useState('');
  const [result, setResult]   = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError]     = useState(null);

  const handleSearch = async () => {
    if (!topic.trim()) return;
    setLoading(true); setError(null); setResult(null);
    try {
      const r = await studyService.getStudyGuide(topic);
      setResult(r.data);
    } catch (e) {
      setError(e.response?.data?.detail || 'Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto py-8">
      <h2 className="text-3xl font-bold text-faith-blue text-center mb-2">
        AI Deep Study Guide
      </h2>
      <p className="text-center text-gray-500 mb-8">
        Sermon prep · Scripture deep-dive · Worship planning · Theological study
      </p>

      <div className="flex flex-wrap gap-2 mb-4">
        {STUDY_SUGGESTIONS.map(s => (
          <button key={s}
            onClick={() => setTopic(s)}
            className={`px-4 py-2 rounded-full text-sm font-medium border transition ${
              topic === s
                ? 'bg-faith-blue text-white border-faith-blue'
                : 'bg-white text-faith-blue border-faith-blue hover:bg-faith-blue hover:text-white'
            }`}
          >{s}</button>
        ))}
      </div>

      <input
        type="text"
        value={topic}
        onChange={e => setTopic(e.target.value)}
        onKeyDown={e => e.key === 'Enter' && handleSearch()}
        placeholder="Enter any topic, verse, character, or question..."
        className="w-full border border-gray-300 rounded-lg p-4 text-gray-700 focus:outline-none focus:border-faith-blue mb-4"
      />

      <button
        onClick={handleSearch}
        disabled={loading || !topic.trim()}
        className="w-full bg-faith-blue text-white py-4 rounded-lg font-semibold text-lg hover:bg-opacity-90 disabled:opacity-50 transition"
      >
        {loading ? 'Studying scripture...' : 'Generate Study Guide'}
      </button>

      {error && (
        <div className="mt-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      {result && (
        <div className="mt-8">
          <h3 className="text-xl font-bold text-faith-blue mb-4">Key Verses</h3>
          {result.verses.map((v, i) => (
            <div key={i} className="bg-spirit-cream border-l-4 border-divine-gold p-5 rounded-lg mb-4">
              <p className="font-semibold text-faith-blue mb-2">{v.reference}</p>
              <p className="font-scripture italic text-gray-800">"{v.text}"</p>
            </div>
          ))}

          <div className="bg-blue-50 border-l-4 border-faith-blue p-6 rounded-lg mt-6">
            <h3 className="font-bold text-faith-blue mb-3">Study Guide</h3>
            <div className="text-gray-700 leading-relaxed whitespace-pre-line">
              {result.study_guide}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
```

#### Step 3.7: Main App Component

```jsx
// src/App.jsx
import React, { useState } from 'react';
import VerseOfDay from './components/VerseOfDay';
import EmotionBasedDevotional from './components/EmotionBasedDevotional';
import AIDeepStudyGuide from './components/AIDeepStudyGuide';

function App() {
  const [page, setPage] = useState('home');

  const navBtn = (id, label) => (
    <button
      onClick={() => setPage(id)}
      className={`px-4 py-2 rounded font-medium transition text-sm ${
        page === id
          ? 'bg-divine-gold text-faith-blue'
          : 'text-spirit-cream hover:text-divine-gold'
      }`}
    >{label}</button>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-spirit-cream via-white to-spirit-cream">
      <nav className="bg-faith-blue shadow-lg sticky top-0 z-50">
        <div className="max-w-5xl mx-auto px-4 py-4 flex justify-between items-center">
          <span className="text-2xl font-bold text-divine-gold cursor-pointer"
            onClick={() => setPage('home')}>
            LogosLight
          </span>
          <div className="flex gap-2">
            {navBtn('home', 'Home')}
            {navBtn('emotion', 'Emotion-Based Devotional')}
            {navBtn('study', 'AI Deep Study Guide')}
          </div>
        </div>
      </nav>

      <main className="max-w-5xl mx-auto px-4 py-8">
        {page === 'home' && (
          <>
            <div className="text-center py-6">
              <h2 className="text-4xl font-bold text-faith-blue mb-2">Welcome to LogosLight</h2>
              <p className="text-gray-600 text-lg">God's Word for every moment of your day</p>
            </div>
            <VerseOfDay />
            <div className="grid md:grid-cols-2 gap-6 mt-8">
              <div onClick={() => setPage('emotion')}
                className="cursor-pointer bg-white rounded-xl shadow p-6 hover:shadow-lg transition border-t-4 border-divine-gold">
                <h3 className="text-xl font-bold text-faith-blue mb-2">Emotion-Based Devotional</h3>
                <p className="text-gray-600">Get scripture, prayer, and encouragement tailored to how you're feeling right now.</p>
              </div>
              <div onClick={() => setPage('study')}
                className="cursor-pointer bg-white rounded-xl shadow p-6 hover:shadow-lg transition border-t-4 border-faith-blue">
                <h3 className="text-xl font-bold text-faith-blue mb-2">AI Deep Study Guide</h3>
                <p className="text-gray-600">Prepare sermons, study topics deeply, plan worship, or explore any Biblical question.</p>
              </div>
            </div>
          </>
        )}
        {page === 'emotion' && <EmotionBasedDevotional />}
        {page === 'study'   && <AIDeepStudyGuide />}
      </main>
    </div>
  );
}

export default App;
```

---

## Database Schema

```
verses table (Supabase / PostgreSQL)
+---------------+--------------+------------------+
| Column        | Type         | Notes            |
+---------------+--------------+------------------+
| id            | UUID         | PRIMARY KEY      |
| book          | VARCHAR(50)  | NOT NULL         |
| chapter       | INT          | NOT NULL         |
| verse_number  | INT          | NOT NULL         |
| text          | TEXT         | NOT NULL         |
| version       | VARCHAR(10)  | DEFAULT 'KJV'    |
| created_at    | TIMESTAMP    | DEFAULT NOW()    |
+---------------+--------------+------------------+

UNIQUE constraint: (book, chapter, verse_number)
INDEX: idx_verses_ref ON (book, chapter, verse_number)

NO VECTOR column.
NO pgvector extension.
NO embedding index.
Standard SQL only.
```

---

## API Specifications

### Base URLs

```
Development:  http://localhost:8000
Production:   https://logos-light-api.onrender.com
API Docs:     http://localhost:8000/docs
```

### Endpoints

#### GET /api/health
```json
{ "status": "healthy", "timestamp": "2026-05-25T10:00:00" }
```

#### GET /api/verses/verse-of-day
```json
{
  "reference": "Psalm 46:1",
  "text": "God is our refuge and strength, a very present help in trouble.",
  "book": "Psalm", "chapter": 46, "verse": 1,
  "reflection": "Meditate on this verse and how God is speaking to you today.",
  "apply_today": "Find one practical way to live out this scripture today."
}
```

#### POST /api/devotional/emotion
```json
// Request
{ "emotion": "I'm anxious about my job interview tomorrow" }

// Response
{
  "emotion": "I'm anxious about my job interview tomorrow",
  "verses": [
    { "reference": "Philippians 4:6", "text": "Be careful for nothing..." },
    { "reference": "Matthew 6:34", "text": "Take therefore no thought..." }
  ],
  "prayer": "Heavenly Father, I come before You with my anxious heart...",
  "encouragement": "God has not given you a spirit of fear...",
  "full_response": "..."
}
```

#### POST /api/ai-study/search
```json
// Request
{ "topic": "Preparing a sermon on grace" }

// Response
{
  "topic": "Preparing a sermon on grace",
  "verses": [
    { "reference": "Ephesians 2:8", "text": "For by grace are ye saved..." }
  ],
  "study_guide": "Overview: ...\n\nVerse Explanations: ...\n\nApplication: ...\n\nReflection Question: ..."
}
```

### Error Responses

```json
{ "detail": "Please describe your emotion" }     // 400
{ "detail": "Could not load verses" }            // 500
```

---

## Deployment Guide

### Step 1: Deploy Backend to Render

```bash
# Create Procfile in backend folder
echo 'web: uvicorn main:app --host 0.0.0.0 --port $PORT' > Procfile
```

1. Push backend folder to GitHub
2. Go to render.com -> New Web Service -> Connect repo
3. Settings:
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Plan: Free
4. Add environment variables:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
   - `ANTHROPIC_API_KEY`
5. Deploy

### Step 2: Deploy Frontend to Vercel

```bash
# frontend/.env
VITE_API_URL=https://your-render-app.onrender.com

npm run build
```

Or connect frontend GitHub repo to vercel.com for auto-deployment on every push.

---

## Testing Strategy

### Backend Tests

```python
# test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"

def test_verse_of_day():
    r = client.get("/api/verses/verse-of-day")
    assert r.status_code == 200
    assert "reference" in r.json()
    assert "text" in r.json()

def test_emotion_devotional():
    r = client.post("/api/devotional/emotion", json={"emotion": "anxious"})
    assert r.status_code == 200
    data = r.json()
    assert "verses" in data
    assert "prayer" in data
    assert "encouragement" in data

def test_open_emotion_input():
    # Should handle any free-text emotion, not just predefined values
    r = client.post("/api/devotional/emotion",
                    json={"emotion": "struggling with my faith after loss"})
    assert r.status_code == 200

def test_deep_study():
    r = client.post("/api/ai-study/search", json={"topic": "grace"})
    assert r.status_code == 200
    assert "study_guide" in r.json()
```

### Quick Curl Tests

```bash
# Health
curl http://localhost:8000/api/health

# Verse of day
curl http://localhost:8000/api/verses/verse-of-day

# Emotion - preset
curl -X POST http://localhost:8000/api/devotional/emotion \
  -H "Content-Type: application/json" \
  -d '{"emotion": "anxious"}'

# Emotion - open input
curl -X POST http://localhost:8000/api/devotional/emotion \
  -H "Content-Type: application/json" \
  -d '{"emotion": "I feel distant from God lately"}'

# Deep study
curl -X POST http://localhost:8000/api/ai-study/search \
  -H "Content-Type: application/json" \
  -d '{"topic": "preparing a sermon on forgiveness"}'
```

---

## Timeline & Milestones

### Week 1: Backend + Database (Days 1-7)
- [ ] Create main.py, database.py, claude.py
- [ ] Configure Supabase - create verses table + get_random_verse function
- [ ] Download KJV JSON and run load_verses.py
- [ ] Test all 3 endpoints locally with curl
- [ ] Deploy backend to Render

### Week 2: Frontend (Days 8-14)
- [ ] Create React + Vite project
- [ ] Configure Tailwind with spiritual color palette
- [ ] Build VerseOfDay component (Home banner)
- [ ] Build EmotionBasedDevotional component (open input)
- [ ] Build AIDeepStudyGuide component
- [ ] Build App.jsx with 3-page navigation
- [ ] Connect all components to backend API
- [ ] Deploy frontend to Vercel

### Week 3: Polish & Launch (Days 15-21)
- [ ] End-to-end testing across all features
- [ ] Mobile responsive check
- [ ] Expand VERSE_MAP with more emotions and topics
- [ ] Fine-tune Claude prompts based on real outputs
- [ ] Public launch

---

## Success Criteria

| Category | Target |
|---|---|
| API response time | < 3 seconds |
| Claude response quality | Warm, scripture-grounded, compassionate |
| Mobile usability | Works on all screen sizes |
| Verse map coverage | 20+ emotions, 15+ study topics |
| Monthly cost | < $5 |

---

## Next Steps

1. Get Anthropic API key - console.anthropic.com
2. Create Supabase project - supabase.com
3. Start with database.py and get_random_verse working
4. Load KJV verses using scripts/load_verses.py
5. Test all endpoints locally, then deploy to Render + Vercel

---

## Resources

- FastAPI: https://fastapi.tiangolo.com/
- Supabase: https://supabase.com/docs
- Anthropic SDK: https://docs.anthropic.com/
- React + Vite: https://vitejs.dev/
- Tailwind CSS: https://tailwindcss.com/
- KJV Bible Data: https://github.com/scrollmapper/bible_databases

---

Build with purpose. LogosLight - God's Word for every moment.

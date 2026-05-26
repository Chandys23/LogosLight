# LogosLight

**God's Word for every moment of your day.**

A free Christian devotional app — KJV scripture + Claude Haiku AI.

---

## Features

- **Verse of the Day** — a fresh KJV verse every visit
- **Emotion-Based Devotional** — share how you're feeling, get scripture + prayer + encouragement
- **AI Deep Study Guide** — sermon prep, topic deep-dives, worship planning

## Tech Stack

| Layer | Tech | Cost |
|---|---|---|
| Frontend | React 18 + Vite + Tailwind | Free (Vercel) |
| Backend | FastAPI (Python) | Free (Render) |
| Database | PostgreSQL (Supabase) | Free (500MB) |
| AI | Claude Haiku (Anthropic) | ~$1–5/month |

## Quick Start

### 1. Supabase Setup

Create a project at [supabase.com](https://supabase.com), then run this SQL:

```sql
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

CREATE INDEX idx_verses_ref ON verses(book, chapter, verse_number);

CREATE OR REPLACE FUNCTION get_random_verse()
RETURNS TABLE(book VARCHAR, chapter INT, verse_number INT, text TEXT)
LANGUAGE sql AS $$
    SELECT book, chapter, verse_number, text FROM verses ORDER BY RANDOM() LIMIT 1;
$$;
```

### 2. Load KJV Bible

```bash
cd scripts
pip install requests python-dotenv supabase
python download_bible.py
python load_verses.py
```

### 3. Run Backend

```bash
cd backend
cp .env.example .env        # fill in your keys
pip install -r requirements.txt
uvicorn main:app --reload
# API runs at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### 4. Run Frontend

```bash
cd frontend
npm install
npm run dev
# App runs at http://localhost:5173
```

## Deploy

- **Backend** → [render.com](https://render.com) (free Web Service, uses Procfile)
- **Frontend** → [vercel.com](https://vercel.com) (free, auto-deploys from GitHub)

Set `VITE_API_URL` in `frontend/.env.production` to your Render URL before deploying.

## Project Structure

```
logos-light/
├── backend/
│   ├── main.py           # FastAPI app + all routes
│   ├── database.py       # Supabase connection + verse lookups
│   ├── claude.py         # Claude Haiku calls + VERSE_MAP + prompts
│   ├── test_main.py      # pytest tests
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── App.jsx
│       ├── components/
│       │   ├── VerseOfDay.jsx
│       │   ├── EmotionBasedDevotional.jsx
│       │   └── AIDeepStudyGuide.jsx
│       └── utils/api.js
└── scripts/
    ├── download_bible.py
    └── load_verses.py
```

---

Built with ❤️ on public-domain KJV scripture.

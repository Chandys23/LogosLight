import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
CLAUDE_MODEL = "claude-haiku-4-5"

# ---------------------------------------------------------------------------
# Curated Verse Map
# Emotion/topic keywords -> hand-picked KJV verse references.
# Claude handles interpretation for anything not in this map.
# ---------------------------------------------------------------------------
VERSE_MAP: dict[str, list[str]] = {
    # Emotions
    "anxious":      ["Philippians 4:6", "Matthew 6:34", "1 Peter 5:7", "Isaiah 41:10"],
    "anxiety":      ["Philippians 4:6", "Matthew 6:34", "1 Peter 5:7", "Isaiah 41:10"],
    "sad":          ["Psalm 34:18", "John 11:35", "Matthew 5:4", "Psalm 147:3"],
    "grief":        ["Psalm 34:18", "John 11:35", "Matthew 5:4", "Revelation 21:4"],
    "lost":         ["Proverbs 3:5", "John 14:6", "Psalm 119:105", "Jeremiah 29:11"],
    "confused":     ["Proverbs 3:5", "James 1:5", "Psalm 32:8", "John 14:6"],
    "grateful":     ["1 Thessalonians 5:18", "Psalm 107:1", "Colossians 3:17"],
    "thankful":     ["1 Thessalonians 5:18", "Psalm 107:1", "Colossians 3:17"],
    "seeking":      ["Matthew 7:7", "Jeremiah 29:13", "Proverbs 8:17", "Psalm 27:4"],
    "joyful":       ["Philippians 4:4", "Psalm 118:24", "John 15:11", "Romans 15:13"],
    "happy":        ["Philippians 4:4", "Psalm 118:24", "John 15:11", "Nehemiah 8:10"],
    "overwhelmed":  ["Matthew 11:28", "Isaiah 40:31", "Psalm 61:2", "2 Corinthians 4:8"],
    "stressed":     ["Matthew 11:28", "Isaiah 40:31", "Philippians 4:7", "Psalm 55:22"],
    "lonely":       ["Hebrews 13:5", "Psalm 68:6", "Isaiah 43:2", "Matthew 28:20"],
    "hopeful":      ["Romans 15:13", "Jeremiah 29:11", "Psalm 31:24", "Hebrews 11:1"],
    "fearful":      ["Isaiah 41:10", "2 Timothy 1:7", "Psalm 27:1", "John 14:27"],
    "afraid":       ["Isaiah 41:10", "2 Timothy 1:7", "Psalm 27:1", "John 14:27"],
    "angry":        ["Ephesians 4:26", "Proverbs 15:1", "James 1:20", "Psalm 37:8"],
    "doubt":        ["Mark 9:24", "James 1:6", "Hebrews 11:1", "Matthew 14:31"],
    "guilty":       ["1 John 1:9", "Romans 8:1", "Psalm 103:12", "Isaiah 43:25"],
    "ashamed":      ["Romans 8:1", "1 John 1:9", "Isaiah 54:4", "Psalm 34:5"],
    "tired":        ["Isaiah 40:31", "Matthew 11:28", "Psalm 23:2", "2 Corinthians 4:16"],
    "weary":        ["Isaiah 40:31", "Matthew 11:28", "Galatians 6:9", "Psalm 23:2"],
    "broken":       ["Psalm 34:18", "Isaiah 61:1", "Matthew 5:4", "Psalm 147:3"],
    # Deep Study Topics
    "faith":        ["Hebrews 11:1", "Romans 10:17", "James 2:17", "Matthew 17:20"],
    "prayer":       ["Matthew 6:9", "1 Thessalonians 5:17", "Philippians 4:6", "James 5:16"],
    "love":         ["1 Corinthians 13:4", "John 3:16", "1 John 4:8", "Romans 8:38"],
    "grace":        ["Ephesians 2:8", "2 Corinthians 12:9", "Romans 5:8", "Titus 2:11"],
    "forgiveness":  ["Ephesians 4:32", "Matthew 6:14", "Colossians 3:13", "1 John 1:9"],
    "strength":     ["Isaiah 40:31", "Philippians 4:13", "Psalm 46:1", "2 Corinthians 12:10"],
    "wisdom":       ["Proverbs 3:5", "James 1:5", "Proverbs 9:10", "Colossians 2:3"],
    "salvation":    ["John 3:16", "Romans 10:9", "Acts 4:12", "Ephesians 2:8"],
    "hope":         ["Romans 15:13", "Jeremiah 29:11", "Romans 8:24", "Lamentations 3:22"],
    "peace":        ["John 14:27", "Philippians 4:7", "Isaiah 26:3", "Romans 5:1"],
    "purpose":      ["Jeremiah 29:11", "Romans 8:28", "Proverbs 16:3", "Ephesians 2:10"],
    "trust":        ["Proverbs 3:5", "Psalm 37:5", "Isaiah 26:3", "Psalm 56:3"],
    "obedience":    ["John 14:15", "Deuteronomy 28:1", "1 Samuel 15:22", "Acts 5:29"],
    "holy spirit":  ["John 14:26", "Acts 1:8", "Romans 8:26", "Galatians 5:22"],
    "resurrection": ["John 11:25", "Romans 6:5", "1 Corinthians 15:55", "Philippians 3:10"],
    "baptism":      ["Matthew 28:19", "Romans 6:4", "Acts 2:38", "Galatians 3:27"],
    "worship":      ["John 4:24", "Psalm 95:6", "Romans 12:1", "Revelation 4:11"],
    "sermon":       ["Romans 10:14", "2 Timothy 4:2", "Isaiah 52:7", "1 Corinthians 1:21"],
}

# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

EMOTION_PROMPT = """\
You are a compassionate Christian spiritual guide. The user is feeling: {emotion}

Here are relevant KJV Bible verses for their situation:
{verses}

Respond with three clearly labeled sections:

**Verse Reflections**
For each verse, write 2-3 sentences explaining how it speaks directly to what the user is feeling.

**Prayer**
Write a heartfelt prayer (3-4 sentences) that begins with "Heavenly Father," and is grounded in the verses above.

**Encouragement**
Write 2-3 sentences of warm, personal encouragement rooted in these scriptures.

Keep your tone compassionate, warm, and strictly grounded in the provided KJV verses."""

AI_DEEP_STUDY_PROMPT = """\
You are a Biblical scholar and pastor preparing study material. The topic or question is: {topic}

Here are key KJV Bible verses on this topic:
{verses}

Respond with four clearly labeled sections:

**Overview**
3-4 sentences summarizing what Scripture teaches about this topic.

**Verse Explanations**
For each verse, write 2-3 sentences explaining its meaning and connection to the topic.

**Application**
3-4 sentences on how this topic applies to daily Christian life, sermon delivery, or congregational discussion.

**Reflection Question**
One thoughtful question for personal study or group discussion.

Ground your response strictly in the provided KJV verses."""


# ---------------------------------------------------------------------------
# Verse reference lookup
# ---------------------------------------------------------------------------

def get_verse_references(query: str) -> list[str]:
    """
    Return curated verse references for a query string.
    Tries exact match, then partial match, then returns general comfort verses.
    Claude handles any emotion or topic — no input is rejected.
    """
    q = query.lower().strip()

    # Exact match
    if q in VERSE_MAP:
        return VERSE_MAP[q]

    # Partial match: query contains a key, or a key contains the query
    for key in VERSE_MAP:
        if key in q or q in key:
            return VERSE_MAP[key]

    # Default: general comfort + guidance verses
    return [
        "Psalm 23:1",
        "John 3:16",
        "Romans 8:28",
        "Philippians 4:13",
        "Isaiah 40:31",
    ]


# ---------------------------------------------------------------------------
# Claude API calls
# ---------------------------------------------------------------------------

def call_claude(prompt: str) -> str:
    """Send a prompt to Claude Haiku and return the text response."""
    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def generate_emotion_devotional(emotion: str, verses: list[dict]) -> dict:
    """Generate prayer, encouragement, and verse reflections for an emotion."""
    verses_text = "\n".join(
        f"- {v['book']} {v['chapter']}:{v['verse_number']}: \"{v['text']}\""
        for v in verses
    )
    prompt = EMOTION_PROMPT.format(emotion=emotion, verses=verses_text)
    response = call_claude(prompt)

    # Extract prayer and encouragement sections for top-level fields
    prayer = ""
    encouragement = ""
    if "Prayer" in response:
        parts = response.split("Prayer")
        prayer = parts[1].split("\n\n")[0].replace("**", "").replace(":", "").strip()
    if "Encouragement" in response:
        parts = response.split("Encouragement")
        encouragement = parts[1].split("\n\n")[0].replace("**", "").replace(":", "").strip()

    return {
        "response": response,
        "prayer": prayer or "Heavenly Father, guide us by Your word. Amen.",
        "encouragement": encouragement or "Trust in God's unfailing love.",
    }


def generate_deep_study(topic: str, verses: list[dict]) -> dict:
    """Generate a deep study guide for a topic."""
    verses_text = "\n".join(
        f"- {v['book']} {v['chapter']}:{v['verse_number']}: \"{v['text']}\""
        for v in verses
    )
    prompt = AI_DEEP_STUDY_PROMPT.format(topic=topic, verses=verses_text)
    response = call_claude(prompt)
    return {"response": response}

import os
import anthropic
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not found")

client = anthropic.Anthropic(api_key=api_key)
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-haiku-4-5")

# Simple, hardcoded verse map (proven to exist in database)
VERSE_MAP = {
    "anxious": ["Psalms 23:1", "John 14:1", "John 14:27"],
    "anxiety": ["Psalms 23:1", "John 14:1", "John 14:27"],
    "sad": ["Psalms 23:1", "Psalms 34:18"],
    "grief": ["Psalms 23:1", "Psalms 34:18"],
    "lonely": ["Psalms 23:4"],
    "fearful": ["Psalms 27:1"],
    "afraid": ["Psalms 27:1"],
    "angry": ["Psalms 37:5"],
    "doubt": ["John 11:25"],
    "guilty": ["Psalms 103:12"],
    "tired": ["Psalms 23:2"],
    "faith": ["John 3:16", "Hebrews 11:1"],
    "prayer": ["Philippians 4:6", "Matthew 7:7"],
    "love": ["John 3:16", "1 Corinthians 13:4"],
    "grace": ["John 1:14", "2 Corinthians 5:17"],
    "strength": ["Psalms 46:1", "Philippians 4:13"],
    "wisdom": ["Psalms 119:105", "James 1:5"],
    "salvation": ["John 3:16", "Romans 6:23"],
    "hope": ["Psalms 31:24", "Romans 8:28"],
    "peace": ["John 14:27", "Philippians 4:7"],
}

def call_claude(prompt: str) -> str:
    """Call Claude and return text response."""
    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def _extract_section(response: str, section_name: str) -> str:
    """Extract section from Claude response. Returns default if not found."""
    lines = response.split("\n")
    defaults = {
        "Prayer": "Heavenly Father, guide us by Your word. Amen.",
        "Encouragement": "Trust in God's unfailing love and faithfulness.",
    }
    
    # Find section header and collect content until next section
    start_idx = None
    for i, line in enumerate(lines):
        if section_name.lower() in line.lower():
            start_idx = i + 1
            break
    
    if start_idx is None:
        return defaults.get(section_name, "")
    
    content = []
    for line in lines[start_idx:]:
        if line.startswith("#") or (line.startswith("**") and section_name not in line):
            break
        if line.strip():
            content.append(line.strip())
    
    return " ".join(content) if content else defaults.get(section_name, "")


def get_verse_references(query: str) -> list[str]:
    """Get verses: exact/partial match from VERSE_MAP, else defaults."""
    q = query.lower().strip()
    
    if q in VERSE_MAP:
        return VERSE_MAP[q]
    
    for key in VERSE_MAP:
        if key in q or q in key:
            return VERSE_MAP[key]
    
    return ["Psalms 23:1", "John 3:16"]


def generate_emotion_devotional(emotion: str, verses: list[dict]) -> dict:
    """Generate prayer + encouragement for an emotion."""
    verses_text = "\n".join(
        f"- {v['book']} {v['chapter']}:{v['verse_number']}: \"{v['text']}\""
        for v in verses
    )
    
    prompt = f"""You are a compassionate Christian spiritual guide. The user is feeling: {emotion}

Here are relevant KJV Bible verses:
{verses_text}

Respond with two sections:

**Prayer**
Write a heartfelt prayer (2-3 sentences) grounded in these verses.

**Encouragement**
Write 2-3 sentences of warm encouragement rooted in Scripture."""
    
    response = call_claude(prompt)
    
    return {
        "response": response,
        "prayer": _extract_section(response, "Prayer"),
        "encouragement": _extract_section(response, "Encouragement"),
    }


def generate_deep_study(topic: str, verses: list[dict]) -> dict:
    """Generate a deep study guide."""
    verses_text = "\n".join(
        f"- {v['book']} {v['chapter']}:{v['verse_number']}: \"{v['text']}\""
        for v in verses
    )
    
    prompt = f"""You are a Biblical scholar. Topic: {topic}

Key verses:
{verses_text}

Provide a concise study with:
- Overview (what Scripture teaches)
- Verse Explanations (meaning of each verse)
- Application (practical takeaway)
- Reflection Question (one thoughtful question)"""
    
    response = call_claude(prompt)
    
    return {"response": response}

"""
Basic tests for the LogosLight API.
Run with: pytest test_main.py -v
"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"


def test_verse_of_day_shape():
    """Verse of day should return the expected fields."""
    r = client.get("/api/verses/verse-of-day")
    assert r.status_code == 200
    data = r.json()
    for field in ("reference", "text", "reflection", "apply_today"):
        assert field in data, f"Missing field: {field}"


def test_emotion_devotional_preset():
    r = client.post("/api/devotional/emotion", json={"emotion": "anxious"})
    assert r.status_code == 200
    data = r.json()
    assert "verses" in data
    assert "prayer" in data
    assert "encouragement" in data
    assert len(data["verses"]) > 0


def test_emotion_devotional_open_input():
    """Should handle any free-text emotion — no rejection."""
    r = client.post(
        "/api/devotional/emotion",
        json={"emotion": "I feel distant from God after a difficult week"},
    )
    assert r.status_code == 200
    assert "verses" in r.json()


def test_emotion_devotional_empty():
    r = client.post("/api/devotional/emotion", json={"emotion": ""})
    assert r.status_code == 400


def test_deep_study_preset():
    r = client.post("/api/ai-study/search", json={"topic": "grace"})
    assert r.status_code == 200
    data = r.json()
    assert "verses" in data
    assert "study_guide" in data
    assert len(data["verses"]) > 0


def test_deep_study_open_input():
    """Should handle sermon prep questions, not just single keywords."""
    r = client.post(
        "/api/ai-study/search",
        json={"topic": "How do I preach on forgiveness to a congregation dealing with conflict?"},
    )
    assert r.status_code == 200


def test_deep_study_empty():
    r = client.post("/api/ai-study/search", json={"topic": ""})
    assert r.status_code == 400

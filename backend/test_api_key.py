#!/usr/bin/env python3
"""
Quick test script to verify Anthropic API key works.
Run from backend/ directory: python test_api_key.py
"""

import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
print(f"API Key loaded: {api_key[:20]}..." if api_key else "NO API KEY FOUND")
print(f"Key starts with 'sk-ant-': {api_key.startswith('sk-ant-') if api_key else False}")

# Try importing Anthropic
try:
    import anthropic
    print("✓ anthropic library imported")
    
    client = anthropic.Anthropic(api_key=api_key)
    print("✓ Anthropic client created")
    
    # Try a simple message
    print("Testing Claude API...")
    message = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=100,
        messages=[{"role": "user", "content": "Say 'Hello from LogosLight!' in 5 words."}],
    )
    print(f"✓ API works! Response: {message.content[0].text}")
    
except Exception as e:
    print(f"✗ Error: {e}")

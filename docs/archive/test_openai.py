#!/usr/bin/env python3
"""Quick test of OpenAI API connection."""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

print(f"🔑 Testing OpenAI API...")
print(f"📦 Model: {model}")
print(f"🔐 API Key: {api_key[:20]}...{api_key[-4:]}")
print()

try:
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'Hello from Project Wizard AI!' in one sentence."}
        ],
        max_tokens=50
    )
    
    message = response.choices[0].message.content
    print(f"✅ SUCCESS! API Response:")
    print(f"   {message}")
    print()
    print(f"📊 Usage: {response.usage.total_tokens} tokens")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    exit(1)

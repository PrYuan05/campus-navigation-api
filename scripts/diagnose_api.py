import os
from google import genai

client = genai.Client(api_key="你的KEY")

# 測測試看 1.5-flash (這在 GCP 區域配額中通常是大於 0 的)
try:
    print("[Test] Trying Gemini 1.5 Flash...")
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents="Hi",
    )
    print(f"[Success] 1.5-flash works!")
except Exception as e:
    print(f"[Failed] 1.5-flash also failed: {e}")

# 再測測試看 2.0-flash
try:
    print("\n[Test] Trying Gemini 2.0 Flash...")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Hi",
    )
    print(f"[Success] 2.0-flash works!")
except Exception as e:
    print(f"[Failed] 2.0-flash failed: {e}")
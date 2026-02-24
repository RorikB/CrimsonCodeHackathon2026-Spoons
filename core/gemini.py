import google.genai as genai
import os
from pathlib import Path
from dotenv import load_dotenv

# Prefer repo config/.env when present, but allow OS env vars as fallback.
dotenv_path = Path(__file__).resolve().parents[1] / "config" / ".env"
if dotenv_path.exists():
    load_dotenv(dotenv_path)
else:
    load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY (or GOOGLE_API_KEY) not found. Set it in environment or config/.env")

client = genai.Client(api_key=GEMINI_API_KEY)

def prompt_gemini(user_input):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=user_input,
        )
        return response.text
    except Exception as e:
        message = str(e)
        if "RESOURCE_EXHAUSTED" in message or "429" in message:
            return "Error: Gemini quota exceeded. Try again in a minute or check your billing/quota."
        return f"Error: {message}"
from google import genai
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
print("Client initialized successfully.")
response = client.models.generate_content(
    model="gemini-3-flash-preview", contents="Explain how AI works in a few words"
)
print(response.text)
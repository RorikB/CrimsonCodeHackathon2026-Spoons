from google import genai
import os
from dotenv import load_dotenv


# Load the environment variables from the .env file
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
print("Client initialized successfully.")
with open('systemprompt.txt', 'r', encoding='utf-8') as f:
    system_prompt = f.read()

def prompt_gemini(input_text):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        # model="gemma-3-1B",
        contents=input_text,
        config={
            "system_instruction": system_prompt
        }
    )
    print(response.text)
    return response.text


# prompt_gemini("What is the first move in chess?")
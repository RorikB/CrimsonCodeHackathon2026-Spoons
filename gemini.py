from google import genai
import os
from dotenv import load_dotenv


# Load the environment variables from the .env file
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
print("Client initialized successfully.")


def prompt_gemini(input_text):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        # model="gemma-3-1B",
        contents=input_text,
        config={
            "system_instruction": "you are a smart mirror that keeps answers concise and accurate" +
            "can call funtion -turnOnLight() in this format, we calling functions only say -turnOnLight() and nothing else"
        }
    )
    print(response.text)
    return response.text


# prompt_gemini("What is the first move in chess?")
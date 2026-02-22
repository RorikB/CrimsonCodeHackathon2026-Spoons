import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# Load weather.env correctly
env_path = Path(__file__).parent.parent / "weather.env"
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("WEATHER_API_KEY")
CITY = os.getenv("CITY", "Pullman")

def get_weather():
    try:
        if not API_KEY:
            return {"error": "WEATHER_API_KEY not found in weather.env"}

        url = (
            f"http://api.openweathermap.org/data/2.5/weather"
            f"?q={CITY}&appid={API_KEY}&units=imperial"
        )

        response = requests.get(url, timeout=10)
        data = response.json()

        if response.status_code != 200:
            return {
                "error": "Failed to fetch weather",
                "api_response": data
            }

        return {
            "city": CITY,
            "temperature": round(data["main"]["temp"]),
            "condition": data["weather"][0]["main"],
            "description": data["weather"][0]["description"],
            "high": round(data["main"]["temp_max"]),
            "low": round(data["main"]["temp_min"]),
            "humidity": data["main"]["humidity"],
            "icon": data["weather"][0]["icon"]
        }

    except Exception as e:
        return {"error": str(e)}
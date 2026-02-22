import os
import requests
from dotenv import load_dotenv

# Load env file
load_dotenv("weather.env")

API_KEY = os.getenv("API_KEY")
CITY = os.getenv("CITY", "Pullman")

def get_weather_data():
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=imperial"
    
    response = requests.get(url, timeout=5)
    data = response.json()

    if "main" not in data:
        return {"error": data}

    return {
        "city": CITY,
        "temperature": round(data["main"]["temp"]),
        "condition": data["weather"][0]["main"],
        "high": round(data["main"]["temp_max"]),
        "low": round(data["main"]["temp_min"]),
        "humidity": data["main"]["humidity"],
        "wind": data["wind"]["speed"]
    }
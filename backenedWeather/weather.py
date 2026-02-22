import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# Absolute path to this file's directory
BASE_DIR = Path(__file__).resolve().parent

# Absolute path to weather.env
env_path = BASE_DIR / "weather.env"

print("Loading .env from:", env_path)
print("Does env exist?", env_path.exists())

load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("API_KEY")
CITY = os.getenv("CITY", "Pullman")

print("Loaded API_KEY:", API_KEY)

def get_weather_data():
    if not API_KEY:
        return {"error": "API key not loaded"}

    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=imperial"
    
    response = requests.get(url, timeout=5)
    data = response.json()

    if response.status_code != 200:
        return {"error": data}

    return {
     "location": CITY,
    "temperature": f'{round(data["main"]["temp"])}°',
    "condition": data["weather"][0]["main"],
    "high": f'{round(data["main"]["temp_max"])}°',
    "low": f'{round(data["main"]["temp_min"])}°',
    "humidity": f'{data["main"]["humidity"]}%',
    "wind_speed": f'{data["wind"]["speed"]} m/s'
    
}

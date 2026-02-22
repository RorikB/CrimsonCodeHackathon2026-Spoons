import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")
CITY = os.getenv("CITY", "Pullman")

def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=imperial"
    
    response = requests.get(url)
    data = response.json()

    return {
        "city": CITY,
        "temperature": round(data["main"]["temp"]),
        "condition": data["weather"][0]["main"],
        "high": round(data["main"]["temp_max"]),
        "low": round(data["main"]["temp_min"]),
        "icon": data["weather"][0]["icon"]
    }
    
    print("API_KEY:", API_KEY)
print("CITY:", CITY)  
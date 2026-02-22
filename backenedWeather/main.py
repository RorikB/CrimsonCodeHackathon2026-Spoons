from fastapi import FastAPI
from services.weather import get_weather
app = FastAPI()

@app.get("/weather")
def weather():
    return get_weather()
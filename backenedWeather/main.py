from fastapi import FastAPI
from weather import get_weather_data

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Weather API is running"}

@app.get("/weather")
def weather():
    return get_weather_data()
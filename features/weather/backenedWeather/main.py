from fastapi import FastAPI
from weather import get_weather_data

app = FastAPI()

@app.get("/weather")
def weather(): 
    return get_weather_data() 
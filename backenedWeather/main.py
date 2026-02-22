from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.weather import get_weather

app = FastAPI()

# Allow frontend (React) to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Weather API is running"}

@app.get("/weather")
def weather():
    return get_weather()
import subprocess
import time
import requests
import tkinter as tk
import os
from pathlib import Path
import sys


# Get absolute backend path safely
BASE_DIR = Path(__file__).resolve().parent
BACKEND_DIR = BASE_DIR.parent / "backenedWeather"

print("Starting backend from:", BACKEND_DIR)

# Add backend folder to Python path
sys.path.append(str(BACKEND_DIR))
from weather import get_weather_data

backend_process = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "main:app", "--port", "8001"],
    cwd=str(BACKEND_DIR)
)

# Wait for backend to start
time.sleep(3)

def get_weather():
    try:
        response = requests.get("http://127.0.0.1:8001/weather", timeout=5)
        print("Status:", response.status_code)
        print("JSON:", response.json())   
        return response.json()
    except Exception as e:
        print("Error connecting to backend:", e)
        return None

def update_weather():
    weather = get_weather()

    print("Weather received in GUI:", weather)

    if weather:
        weather_label.config(text=str(weather))
    else:
        weather_label.config(text="No response")

    root.after(600000, update_weather)

def on_close():
    backend_process.terminate()
    root.destroy()

# GUI
root = tk.Tk()
root.title("Smart Mirror")
root.geometry("500x400")
root.configure(bg="black")

weather_label = tk.Label(
    root,
    font=("Helvetica", 22),
    fg="white",
    bg="black",
    justify="center"
)

weather_label.pack(expand=True)

update_weather()

root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()
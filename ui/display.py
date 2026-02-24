
import tkinter as tk
from datetime import datetime
from timer import Timer

# from fastapi import requests

from backenedWeather.weather import get_weather_data
from backenedWeather.google_calendar_api import GoogleCalendarAPI

from spotify_widget import SpotifyWidget

import vision
import whisper
import threading

face_detected = False

def run_vision():
   while True:
       result = vision.check_for_face()
       global face_detected
       face_detected = result
def run_whisper():
   while True:
       whisper.speech_to_text()

# --- Placeholder Values ---
PLACEHOLDER_TIME = "12:00 PM"
PLACEHOLDER_DATE = "Sunday, February 22, 2026"
PLACEHOLDER_TEMP = "72°F"
PLACEHOLDER_WEATHER = "Partly Cloudy"
PLACEHOLDER_WEATHER_ICON = "⛅"
PLACEHOLDER_HUMIDITY = "Humidity: 55%"
PLACEHOLDER_WIND = "Wind: 8 mph"
PLACEHOLDER_NAME = "Welcome, User"
PLACEHOLDER_CALENDAR = "No events today"

class SmartMirror(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart Mirror")
        self.configure(bg="black")
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.destroy())

        self._fade_brightness = 0     
        self._fade_direction = 1       
        self._fade_paused = False

        self.calendar = GoogleCalendarAPI()
        self.calendar_ready = self.calendar.authenticate()

        self.timer = Timer()
        self.timer.start(100)

        self.build_ui()
        self.update_clock()
        self.update_weather()
        self.update_calendar()
        self.update_timer_display()
        self.after(300, self.fade_greeting)

    def build_ui(self):
        # ── Top Row ──────────────────────────────────────────────
        top_frame = tk.Frame(self, bg="black")
        top_frame.pack(fill="x", padx=40, pady=30)

        left_frame = tk.Frame(top_frame, bg="black")
        left_frame.pack(side="left")


        self.time_label = tk.Label(
            left_frame, text=PLACEHOLDER_TIME,
            font=("Helvetica Neue", 72, "bold"),
            fg="white", bg="black"
        )
        self.time_label.pack(anchor="w")

        self.date_label = tk.Label(
            left_frame, text=PLACEHOLDER_DATE,
            font=("Helvetica Neue", 22),
            fg="#AAAAAA", bg="black"
        )
        self.date_label.pack(anchor="w")

        right_frame = tk.Frame(top_frame, bg="black")
        right_frame.pack(side="right")

        self.weather_icon_label = tk.Label(right_frame, text=PLACEHOLDER_WEATHER_ICON,
                                   font=("Helvetica Neue", 52), fg="white", bg="black")
        self.weather_icon_label.pack(anchor="e")

        self.weather_temp_label = tk.Label(right_frame, text=PLACEHOLDER_TEMP,
                                   font=("Helvetica Neue", 52, "bold"), fg="white", bg="black")
        self.weather_temp_label.pack(anchor="e")

        self.weather_condition_label = tk.Label(right_frame, text=PLACEHOLDER_WEATHER,
                                        font=("Helvetica Neue", 20), fg="#AAAAAA", bg="black")
        self.weather_condition_label.pack(anchor="e")

        self.weather_humidity_label = tk.Label(right_frame, text=PLACEHOLDER_HUMIDITY,
                                      font=("Helvetica Neue", 16), fg="#888888", bg="black")
        self.weather_humidity_label.pack(anchor="e")

        self.weather_wind_label = tk.Label(right_frame, text=PLACEHOLDER_WIND,
                                   font=("Helvetica Neue", 16), fg="#888888", bg="black")
        self.weather_wind_label.pack(anchor="e")

        # # ── Divider ──────────────────────────────────────────────
        # tk.Frame(self, bg="#333333", height=1).pack(fill="x", padx=40)

        # ── Greeting ─────────────────────────────────────────────
        greeting_frame = tk.Frame(self, bg="black")
        greeting_frame.pack(pady=40)

        self.greeting_label = tk.Label(
            greeting_frame, text=PLACEHOLDER_NAME,
            font=("Helvetica Neue", 48, "italic"),
            fg="#000000", bg="black"   # start invisible
        )
        self.greeting_label.pack()

        # # ── Divider ──────────────────────────────────────────────
        # tk.Frame(self, bg="#333333", height=1).pack(fill="x", padx=40)

        
        # ── News Feed ─────────────────────────────────────────────
        news_frame = tk.Frame(self, bg="black")
        news_frame.pack(fill="x", padx=40, pady=30, side="bottom")

        # ── Timer Display (above calendar)
        self.timer_label = tk.Label(
            news_frame,  # pack inside the same frame as calendar
            text="",
            font=("Helvetica Neue", 48, "bold"),
            fg="#00FFAA",
            bg="black"
        )
        self.timer_label.pack(anchor="w", pady=(0, 10))  # small bottom margin

        tk.Label(news_frame, text="Calendar",
            font=("Helvetica Neue", 16, "bold"),  # increase heading font
            fg="#555555", bg="black").pack(anchor="w", pady=(0,5))  # add small bottom padding

        self.calendar_label = tk.Label(
            news_frame,
            text="Loading events...",
            font=("Helvetica Neue", 18),          # slightly bigger font
            fg="#AAAAAA",
            bg="black",
            wraplength=1000,                       # increase width so it can display more text per line
            justify="left",
            pady=10                                # add vertical padding to give more height
        )
        self.calendar_label.pack(anchor="w", pady=(0, 40))


        # ── Spotify Widget ───────────────────────────────────────  
        self.spotify_widget = SpotifyWidget(self, width=300, height=260, enable_voice=True)
        self.spotify_widget.frame.place(relx=1.0, rely=1.0, anchor="se", x=0, y=80)

    # ── Clock ─────────────────────────────────────────────────────
    def update_clock(self):
        now = datetime.now()
        self.time_label.config(text=now.strftime("%I:%M %p"))
        self.date_label.config(text=now.strftime("%A, %B %d, %Y"))
        self.after(1000, self.update_clock)

    def update_weather(self):
        weather = get_weather_data()
        if "error" in weather:
            self.weather_temp_label.config(text="Weather unavailable")
            self.weather_condition_label.config(text="")
            self.weather_humidity_label.config(text="")
            self.weather_wind_label.config(text="")
        else:
            self.weather_temp_label.config(text=weather["temperature"])
            self.weather_condition_label.config(text=weather["condition"])
            self.weather_humidity_label.config(text=f"Humidity: {weather['humidity']}")
            self.weather_wind_label.config(text=f"Wind: {weather['wind_speed']}")

        # Schedule next update in 10 minutes (600000 ms)
        self.after(600000, self.update_weather)

    def update_calendar(self):
        if not self.calendar_ready:
            self.calendar_label.config(text="Calendar unavailable")
            return

        events = self.calendar.get_todays_events()

        if not events:
            display_text = "No events today"
        else:
            lines = []
            for event in events:
                start = event['start']

                # Convert Google time → readable time
                if "T" in start:
                    dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
                    time_str = dt.strftime("%I:%M %p")
                else:
                    time_str = "All Day"

                title = event['title']
                lines.append(f"{time_str} – {title}")

            display_text = "\n".join(lines)

        self.calendar_label.config(text=display_text)
        self.after(600000, self.update_calendar)

    def update_timer_display(self):
        if self.timer.is_active():
            remaining = self.timer.get_remaining_time()
            minutes = remaining // 60
            seconds = remaining % 60
            self.timer_label.config(text=f"{minutes:02}:{seconds:02}")
        else:
            self.timer_label.config(text="")

        self.after(500, self.update_timer_display)

    # ── Smooth fade in / pause / fade out ────────────────────
    def fade_greeting(self):
        FADE_SPEED = 4          # brightness change per tick (lower = smoother)
        TICK_MS   = 16          # ~60fps
        PAUSE_MS  = 1500        # how long to stay fully visible

        if self._fade_paused:
            return

        self._fade_brightness += FADE_SPEED * self._fade_direction
        self._fade_brightness = max(0, min(255, self._fade_brightness))

        v = self._fade_brightness
        color = f"#{v:02X}{v:02X}{v:02X}"
        self.greeting_label.config(fg=color)

        if self._fade_direction == 1 and self._fade_brightness >= 255:
            # Fully visible — pause before fading out
            self._fade_paused = True
            self.after(PAUSE_MS, self._resume_fade_out)
        elif self._fade_direction == -1 and self._fade_brightness <= 0:
            # Fully invisible — stop the animation.
            # The label is now permanently black on a black background.
            pass
        else:
            self.after(TICK_MS, self.fade_greeting)

    def _resume_fade_out(self):
        self._fade_direction = -1
        self._fade_paused = False
        self.fade_greeting()

if __name__ == "__main__":
       # vision_thread = threading.Thread(target=run_vision, daemon=True)
    whisper_thread = threading.Thread(target=run_whisper, daemon=True)


   # vision_thread.start()
    whisper_thread.start()
    app = SmartMirror()
    app.mainloop()
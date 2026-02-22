# main.py

import tkinter as tk
from timer import Timer
from clock_gui import ClockGUI
import weatherGUI as weatherGUI
from calendar import get_todays_events
from spotify_player import SpotifyPlayer

class SmartMirrorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart Mirror")
        
        self.configure(bg="black")
        self.attributes('-fullscreen', True)
        self.bind("<Escape>", lambda e: self.destroy())

        # Left frame: Clock + Timer
        left_frame = tk.Frame(self, bg="black")
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)

        self.clock_label = tk.Label(left_frame, font=("Helvetica", 48), fg="white", bg="black")
        self.clock_label.pack(pady=10)

        self.timer_label = tk.Label(left_frame, font=("Helvetica", 36), fg="white", bg="black")
        self.timer_label.pack(pady=10)

        # Top-right: Weather
        self.weather_label = tk.Label(self, font=("Helvetica", 20), fg="white", bg="black")
        self.weather_label.pack(side=tk.TOP, anchor="ne", padx=20, pady=20)

        # Bottom-right: Calendar
        self.calendar_label = tk.Label(self, font=("Helvetica", 16), fg="white", bg="black", justify=tk.LEFT)
        self.calendar_label.pack(side=tk.BOTTOM, anchor="se", padx=20, pady=20)

        # Center: Spotify
        self.spotify_label = tk.Label(self, font=("Helvetica", 20), fg="white", bg="black")
        self.spotify_label.pack(expand=True)

        # Initialize backend objects
        self.clock = ClockGUI()
        self.timer = Timer()
        self.spotify = SpotifyPlayer()

        # Start update loops
        self.update_clock()
        self.update_timer()
        self.update_weather()
        self.update_calendar()
        self.update_spotify()

    def update_clock(self):
        self.clock_label.config(text=self.clock.get_time_string())
        self.after(1000, self.update_clock)

    def update_timer(self):
        self.timer_label.config(text=self.timer.get_remaining_time())
        self.after(1000, self.update_timer)

    def update_weather(self):
        data = weatherGUI.get_weather()
        self.weather_label.config(text=f"{data['location']}: {data['temp']}°C, {data['condition']}")
        self.after(30000, self.update_weather)

    def update_calendar(self):
        events = get_todays_events()
        self.calendar_label.config(text="Today's Events:\n" + "\n".join(events))
        self.after(300000, self.update_calendar)

    def update_spotify(self):
        track = self.spotify.get_current_track()
        self.spotify_label.config(text=f"Now Playing:\n{track['artist']} - {track['title']}")
        self.after(2000, self.update_spotify)


if __name__ == "__main__":
    app = SmartMirrorApp()
    app.mainloop()
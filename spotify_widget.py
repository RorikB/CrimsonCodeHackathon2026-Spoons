import os
import threading
import time
import requests
import psutil
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image, ImageTk
from io import BytesIO
import tkinter as tk
from dotenv import load_dotenv

load_dotenv()

try:
    import speech_recognition as sr
    SPEECH_AVAILABLE = True
except Exception:
    SPEECH_AVAILABLE = False


class SpotifyWidget:
    def __init__(self, parent, width=300, height=260, enable_voice=True):
        self.parent = parent
        self.width = width
        self.height = height
        self.enable_voice = enable_voice and SPEECH_AVAILABLE
        self.sp = None
        self.current_track = None
        self.album_image = None
        self.running = True

        self.frame = tk.Frame(parent, bg="black", width=width, height=height)
        self.frame.pack_propagate(False)

        self.title_label = tk.Label(
            self.frame, text="SPOTIFY", font=("Helvetica Neue", 14, "bold"),
            fg="#1DB954", bg="black"
        )
        self.title_label.pack(anchor="w")

        row_frame = tk.Frame(self.frame, bg="black")
        row_frame.pack(fill="x", pady=8)

        self.album_label = tk.Label(row_frame, bg="black")
        self.album_label.pack(side="left")

        text_frame = tk.Frame(row_frame, bg="black")
        text_frame.pack(side="left", fill="both", expand=True, padx=(10, 0))

        text_wrap = max(100, width - 150)
        self.track_label = tk.Label(
            text_frame, text="Not connected", font=("Helvetica Neue", 12),
            fg="white", bg="black", wraplength=text_wrap, justify="left"
        )
        self.track_label.pack(anchor="w")

        self.artist_label = tk.Label(
            text_frame, text="", font=("Helvetica Neue", 10),
            fg="#AAAAAA", bg="black", wraplength=text_wrap, justify="left"
        )
        self.artist_label.pack(anchor="w")

        self.status_label = tk.Label(
            text_frame, text="", font=("Helvetica Neue", 10),
            fg="#888888", bg="black"
        )
        self.status_label.pack(anchor="w", pady=(6, 0))

        threading.Thread(target=self._init_spotify, daemon=True).start()

        if self.enable_voice:
            threading.Thread(target=self._voice_loop, daemon=True).start()

    def _init_spotify(self):
        try:
            client_id = os.getenv("SPOTIFY_CLIENT_ID")
            client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
            redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")

            if not client_id or not client_secret or not redirect_uri:
                self._set_status("Missing Spotify credentials")
                return

            scope = "user-read-playback-state user-modify-playback-state user-read-currently-playing"
            self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri,
                scope=scope,
                open_browser=True,
                cache_path=".spotify_cache"
            ))

            self._ensure_spotify_running()
            self._set_status("Connected")
            self._schedule_update()
        except Exception as e:
            self._set_status(f"Spotify error: {e}")

    def _set_status(self, text):
        self.parent.after(0, lambda: self.status_label.config(text=text))

    def _schedule_update(self):
        if self.running:
            self.parent.after(2000, self._update_track)

    def _update_track(self):
        if not self.sp:
            self._schedule_update()
            return

        self.current_track = self._get_current_track()
        if self.current_track:
            self._update_ui(self.current_track)
        else:
            self._set_status("No track playing")

        self._schedule_update()

    def _update_ui(self, track):
        title = track["name"]
        artist = track["artist"]
        status = "[>] Playing" if track["is_playing"] else "[||] Paused"

        self.parent.after(0, lambda: self.track_label.config(text=title))
        self.parent.after(0, lambda: self.artist_label.config(text=artist))
        self.parent.after(0, lambda: self.status_label.config(text=status))

        if track.get("image_url"):
            image = self._fetch_album_image(track["image_url"])
            if image:
                self.album_image = ImageTk.PhotoImage(image)
                self.parent.after(0, lambda: self.album_label.config(image=self.album_image))
        else:
            self.parent.after(0, lambda: self.album_label.config(image=""))

    def _fetch_album_image(self, url):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content)).convert("RGB")
            return img.resize((110, 110))
        except Exception:
            return None

    def _get_current_track(self):
        try:
            playback = self.sp.current_playback()
            if playback and playback.get("item"):
                track = playback["item"]
                return {
                    "name": track["name"],
                    "artist": track["artists"][0]["name"] if track["artists"] else "Unknown",
                    "album": track["album"]["name"],
                    "image_url": track["album"]["images"][0]["url"] if track["album"]["images"] else None,
                    "is_playing": playback.get("is_playing", False)
                }
        except Exception:
            return None
        return None

    def _ensure_spotify_running(self):
        if self._is_spotify_running():
            return
        try:
            os.startfile("spotify:")
            time.sleep(3)
        except Exception:
            pass

    def _is_spotify_running(self):
        try:
            for proc in psutil.process_iter(["name"]):
                if proc.info["name"] and proc.info["name"].lower() == "spotify.exe":
                    return True
        except Exception:
            pass
        return False

    def play_pause(self):
        try:
            playback = self.sp.current_playback()
            if playback is None or playback.get("device") is None:
                devices = self.sp.devices()
                if devices and devices.get("devices"):
                    device_id = devices["devices"][0]["id"]
                    self.sp.start_playback(device_id=device_id)
                    return
                return
            device_id = playback["device"]["id"]
            if playback.get("is_playing"):
                self.sp.pause_playback(device_id=device_id)
            else:
                self.sp.start_playback(device_id=device_id)
        except Exception:
            pass

    def next_track(self):
        try:
            playback = self.sp.current_playback()
            if playback is None or playback.get("device") is None:
                devices = self.sp.devices()
                if not devices or not devices.get("devices"):
                    return
                device_id = devices["devices"][0]["id"]
            else:
                device_id = playback["device"]["id"]
            self.sp.next_track(device_id=device_id)
        except Exception:
            pass

    def previous_track(self):
        try:
            playback = self.sp.current_playback()
            if playback is None or playback.get("device") is None:
                devices = self.sp.devices()
                if not devices or not devices.get("devices"):
                    return
                device_id = devices["devices"][0]["id"]
            else:
                device_id = playback["device"]["id"]
            self.sp.previous_track(device_id=device_id)
        except Exception:
            pass

    def _voice_loop(self):
        recognizer = sr.Recognizer()
        while self.running:
            try:
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.4)
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
                text = recognizer.recognize_google(audio).lower()

                if "play" in text or "pause" in text:
                    self.play_pause()
                elif "next" in text or "skip" in text:
                    self.next_track()
                elif "previous" in text or "back" in text:
                    self.previous_track()
            except Exception:
                continue

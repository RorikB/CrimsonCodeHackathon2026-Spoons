import cv2
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import threading
import requests
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import os
import subprocess
import psutil
import time

load_dotenv()

class SpotifyPlayer:
    def __init__(self, width=600, height=700):
        self.width = width
        self.height = height
        self.running = True
        
        # Initialize Spotify with playback control
        self.scope = "user-read-playback-state user-modify-playback-state user-read-currently-playing"
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')
        
        if not self.client_id or not self.client_secret:
            raise ValueError("SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET must be set in .env file")
        
        print("Connecting to Spotify...")
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=self.scope,
            open_browser=True,
            cache_path=".spotify_cache"  # Save token to remember login
        ))

        
        
        self.current_track = None
        self.album_cover = None
        self.update_thread = None
        
        # Check and open Spotify if needed
        self.ensure_spotify_running()
    
    def is_spotify_running(self):
        """Check if Spotify is currently running"""
        try:
            for proc in psutil.process_iter(['name']):
                if proc.info['name'].lower() == 'spotify.exe':
                    return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
        return False
    
    def open_spotify(self):
        """Open Spotify application - finds it automatically across Windows"""
        try:
            # First, try to open via protocol handler (most reliable)
            try:
                os.startfile("spotify:")
                print("Launching Spotify via protocol handler...")
                time.sleep(5)
                return True
            except:
                pass
            
            # Search common Spotify installation paths
            possible_paths = [
                os.path.join(os.getenv('APPDATA', ''), "Spotify", "Spotify.exe"),
                "C:\\Program Files\\Spotify\\Spotify.exe",
                "C:\\Program Files (x86)\\Spotify\\Spotify.exe",
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    subprocess.Popen([path], shell=False)
                    print(f"Opening Spotify from: {path}")
                    time.sleep(5)
                    return True
            
            # If not found in common paths, search the entire system
            print("Searching for Spotify installation...")
            import subprocess
            result = subprocess.run(
                ['where', 'Spotify.exe'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                spotify_path = result.stdout.strip().split('\n')[0]
                subprocess.Popen([spotify_path], shell=False)
                print(f"Opening Spotify from: {spotify_path}")
                time.sleep(5)
                return True
        
        except Exception as e:
            print(f"Could not auto-open Spotify: {e}")
        
        return False
    
    def ensure_spotify_running(self):
        """Ensure Spotify is running, open if needed"""
        if not self.is_spotify_running():
            print("Spotify not detected. Opening it automatically...")
            self.open_spotify()
            
            # Wait and check if it's running
            for i in range(10):  # Try for up to 10 seconds
                if self.is_spotify_running():
                    print("✓ Spotify is now running!")
                    return
                time.sleep(1)
            
            print("⚠ Spotify may not have started. Please open it manually if needed.")
        
    def get_current_track(self):
        """Fetch current playing track from Spotify"""
        try:
            playback = self.sp.current_playback()
            if playback and playback['item']:
                track = playback['item']
                return {
                    'name': track['name'],
                    'artist': track['artists'][0]['name'] if track['artists'] else 'Unknown',
                    'album': track['album']['name'],
                    'image_url': track['album']['images'][0]['url'] if track['album']['images'] else None,
                    'is_playing': playback['is_playing']
                }
        except Exception as e:
            print(f"Error fetching track: {e}")
        return None
    
    def fetch_album_cover(self, url):
        """Fetch and convert album cover to OpenCV format"""
        try:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            img = img.resize((300, 300))
            img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            return img_cv
        except Exception as e:
            print(f"Error fetching album cover: {e}")
            return None
    
    def update_track_info(self):
        """Background thread to update track info"""
        while self.running:
            self.current_track = self.get_current_track()
            if self.current_track and self.current_track['image_url']:
                self.album_cover = self.fetch_album_cover(self.current_track['image_url'])
            import time
            time.sleep(2)  # Update every 2 seconds
    
    def play_pause(self):
        """Toggle play/pause - works even without active device"""
        try:
            playback = self.sp.current_playback()
            
            # If no playback info, try to get available devices
            if playback is None or playback['device'] is None:
                devices = self.sp.devices()
                if devices and devices['devices']:
                    # Use the first available device
                    device_id = devices['devices'][0]['id']
                    self.sp.start_playback(device_id=device_id)
                    print("▶ Playing on: " + devices['devices'][0]['name'])
                    time.sleep(0.3)
                    return
                else:
                    print("⚠ No Spotify devices found. Open Spotify app first.")
                    return
            
            device_id = playback['device']['id']
            if playback['is_playing']:
                self.sp.pause_playback(device_id=device_id)
                print("⏸ Paused")
            else:
                self.sp.start_playback(device_id=device_id)
                print("▶ Playing")
            
            time.sleep(0.3)
            self.current_track = self.get_current_track()
        except Exception as e:
            print(f"Error toggling playback: {e}")
    
    def next_track(self):
        """Skip to next track - works even without active device"""
        try:
            playback = self.sp.current_playback()
            
            if playback is None or playback['device'] is None:
                devices = self.sp.devices()
                if not devices or not devices['devices']:
                    print("⚠ No Spotify devices found. Open Spotify app first.")
                    return
                device_id = devices['devices'][0]['id']
            else:
                device_id = playback['device']['id']
            
            self.sp.next_track(device_id=device_id)
            print("⏭ Next track")
            time.sleep(0.5)
            self.current_track = self.get_current_track()
        except Exception as e:
            print(f"Error skipping track: {e}")
    
    def previous_track(self):
        """Go to previous track - works even without active device"""
        try:
            playback = self.sp.current_playback()
            
            if playback is None or playback['device'] is None:
                devices = self.sp.devices()
                if not devices or not devices['devices']:
                    print("⚠ No Spotify devices found. Open Spotify app first.")
                    return
                device_id = devices['devices'][0]['id']
            else:
                device_id = playback['device']['id']
            
            self.sp.previous_track(device_id=device_id)
            print("⏮ Previous track")
            time.sleep(0.5)
            self.current_track = self.get_current_track()
        except Exception as e:
            print(f"Error going to previous track: {e}")
    
    def draw_player(self, frame):
        """Draw the Spotify player display"""
        cv2.rectangle(frame, (0, 0), (self.width, self.height), (20, 20, 20), -1)
        
        # Title
        cv2.putText(frame, "SPOTIFY PLAYER", (self.width//2 - 120, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (31, 177, 76), 2)
        
        if self.current_track:
            y_offset = 80
            
            # Album cover
            if self.album_cover is not None:
                cover_h, cover_w = self.album_cover.shape[:2]
                x_start = (self.width - cover_w) // 2
                y_start = y_offset
                frame[y_start:y_start+cover_h, x_start:x_start+cover_w] = self.album_cover
                y_offset += cover_h + 20
            
            # Song title
            title = self.current_track['name']
            if len(title) > 40:
                title = title[:37] + "..."
            cv2.putText(frame, f"Title: {title}", (20, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 1)
            y_offset += 30
            
            # Artist
            artist = self.current_track['artist']
            if len(artist) > 40:
                artist = artist[:37] + "..."
            cv2.putText(frame, f"Artist: {artist}", (20, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 1)
            y_offset += 30
            
            # Album
            album = self.current_track['album']
            if len(album) > 40:
                album = album[:37] + "..."
            cv2.putText(frame, f"Album: {album}", (20, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 1)
            y_offset += 30
            
            # Status
            status = "[>] Playing" if self.current_track['is_playing'] else "[||] Paused"
            status_color = (0, 255, 0) if self.current_track['is_playing'] else (255, 255, 0)
            cv2.putText(frame, status, (20, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 2)
        else:
            cv2.putText(frame, "No track playing", (50, 200),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 100, 100), 2)
            
            if not self.is_spotify_running():
                cv2.putText(frame, "Opening Spotify...", (20, 260),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (150, 150, 150), 1)
            else:
                cv2.putText(frame, "Start playing music on Spotify", (20, 260),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (150, 150, 150), 1)
                cv2.putText(frame, "or press SPACE to resume", (20, 290),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (150, 150, 150), 1)
        
        # Instructions
        cv2.putText(frame, "SPACE: Play/Pause | N: Next | P: Previous | ESC: Exit", (20, self.height - 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 100, 100), 1)
        
        return frame
    
    def run(self):
        """Run the Spotify player"""
        print("Starting Spotify Player...")
        print("Controls: SPACE=Play/Pause | N=Next | P=Previous | ESC=Exit")
        
        # Start background thread for updating track info
        self.update_thread = threading.Thread(target=self.update_track_info, daemon=True)
        self.update_thread.start()
        
        while self.running:
            frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            frame = self.draw_player(frame)
            
            cv2.imshow("Spotify Player", frame)
            
            key = cv2.waitKey(500) & 0xFF
            
            if key == 27:  # ESC to quit
                self.running = False
            elif key == 32:  # SPACE for play/pause
                self.play_pause()
            elif key == ord('n'):  # N for next track
                self.next_track()
            elif key == ord('p'):  # P for previous track
                self.previous_track()
        
        cv2.destroyAllWindows()
        print("Spotify Player closed")

if __name__ == "__main__":
    player = SpotifyPlayer()
    player.run()

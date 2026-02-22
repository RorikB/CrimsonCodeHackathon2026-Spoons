import cv2
import numpy as np
import subprocess
import os
import threading
from yt_dlp import YoutubeDL
import time

class YouTubeSearchGUI:
    def __init__(self, width=600, height=400):
        self.width = width
        self.height = height
        self.search_text = ""
        self.cursor_pos = 0
        self.searching = False
        self.result_title = None
        
    def draw_input_screen(self, frame):
        """Draw the search input screen"""
        cv2.rectangle(frame, (0, 0), (self.width, self.height), (20, 20, 20), -1)
        
        # Title
        cv2.putText(frame, "YOUTUBE SEARCH", (self.width//2 - 130, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 2)
        
        # Input box
        cv2.rectangle(frame, (40, 120), (self.width - 40, 170), (50, 50, 50), 2)
        cv2.putText(frame, "Search:", (50, 110),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 1)
        
        # Display search text with cursor
        display_text = self.search_text[:35] if len(self.search_text) > 35 else self.search_text
        cv2.putText(frame, display_text, (50, 155),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 1)
        
        # Cursor - taller and better aligned with text
        cursor_x = 50 + len(display_text) * 12
        cv2.line(frame, (cursor_x, 130), (cursor_x, 165), (100, 200, 255), 2)
        
        # Status
        y_pos = 220
        if self.searching:
            cv2.putText(frame, "Searching YouTube...", (60, y_pos),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 200, 255), 1)
        elif self.result_title:
            # Clear search box text display when showing result
            cv2.putText(frame, " " * 40, (50, 155),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 1)
            
            cv2.putText(frame, f"Found: {self.result_title[:45]}", (40, y_pos),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.65, (100, 255, 100), 1)
            y_pos += 40
            cv2.putText(frame, "Press ENTER to play or ESC to search again", (40, y_pos),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (150, 150, 150), 1)
        
        # Instructions
        cv2.putText(frame, "Type search query, press ENTER to search", (40, self.height - 80),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (150, 150, 150), 1)
        cv2.putText(frame, "ESC to exit", (40, self.height - 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (150, 150, 150), 1)
        
        return frame

class YouTubePlayer:
    def __init__(self, width=600, height=700):
        self.width = width
        self.height = height
        self.running = True
        self.video_url = None
        self.video_title = None
        self.video_process = None
        self.is_playing = False
        self.search_mode = True
        self.search_gui = YouTubeSearchGUI(width, 400)
        self.result_found = False  # Track when search result is ready for user action
        
    def search_youtube(self, query):
        """Search for a YouTube video and return the URL"""
        try:
            print(f"Searching for: {query}")
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'default_search': 'ytsearch1',
                'format': 'best[ext=mp4]',
                'socket_timeout': 30,
            }
            
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(query, download=False)
                if info:
                    self.video_url = info.get('url') or info.get('webpage_url')
                    self.video_title = info.get('title', 'Unknown Video')
                    return True
        except Exception as e:
            print(f"Error searching YouTube: {e}")
        return False
    
    def play_video(self):
        """Play the video using VLC in background"""
        if not self.video_url:
            return False
        
        try:
            print(f"Playing: {self.video_title}")
            vlc_path = "vlc"
            
            # Try to find VLC installation
            possible_paths = [
                "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe",
                "C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe",
                "vlc"
            ]
            
            vlc_found = False
            for path in possible_paths:
                if os.path.exists(path):
                    vlc_path = path
                    vlc_found = True
                    break
                elif path == "vlc":
                    vlc_found = True
            
            if vlc_found:
                self.video_process = subprocess.Popen(
                    [vlc_path, self.video_url, "--fullscreen=no", "-I", "dummy", "--play-and-exit"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                self.is_playing = True
                return True
        except Exception as e:
            print(f"Error playing video: {e}")
        
        return False
    
    def stop_video(self):
        """Stop the currently playing video"""
        if self.video_process:
            try:
                self.video_process.terminate()
                self.video_process.wait(timeout=2)
            except:
                self.video_process.kill()
            self.is_playing = False
            self.video_process = None
    
    def draw_player_screen(self, frame):
        """Draw the video player display"""
        cv2.rectangle(frame, (0, 0), (self.width, self.height), (20, 20, 20), -1)
        
        # Title
        cv2.putText(frame, "YOUTUBE PLAYER", (self.width//2 - 130, 50),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 2)
        
        if self.video_title:
            y_offset = 120
            
            # Video title
            title = self.video_title
            if len(title) > 60:
                title = title[:57] + "..."
            cv2.putText(frame, title, (20, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 1)
            y_offset += 50
            
            # Status
            status = "[>] Playing" if self.is_playing else "[||] Stopped"
            status_color = (0, 255, 0) if self.is_playing else (100, 100, 100)
            cv2.putText(frame, status, (20, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 2)
            y_offset += 60
            
            # Info
            cv2.putText(frame, "Playing in VLC (minimize this window to watch)", (20, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (150, 150, 150), 1)
        else:
            cv2.putText(frame, "No video selected", (50, 200),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 100, 100), 2)
        
        # Instructions
        cv2.putText(frame, "S: Search | ESC: Exit", (20, self.height - 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 100, 100), 1)
        
        return frame
    
    def search_thread(self, query):
        """Run search in background thread"""
        if self.search_youtube(query):
            self.search_gui.result_title = self.video_title
            self.result_found = True  # Signal that result is ready
            print(f"Found: {self.video_title}")
        else:
            self.search_gui.result_title = None
            self.result_found = False
            print("Video not found")
        self.search_gui.searching = False
    
    def run(self):
        """Run the YouTube player with GUI"""
        print("Starting YouTube Player...")
        print("Controls: Type search query | ENTER to search | ESC to exit")
        
        while self.running:
            if self.search_mode:
                # If result found, show it and wait for user action
                if self.result_found:
                    frame = np.zeros((self.search_gui.height, self.search_gui.width, 3), dtype=np.uint8)
                    frame = self.search_gui.draw_input_screen(frame)
                    cv2.imshow("YouTube Search", frame)
                    
                    key = cv2.waitKey(100) & 0xFF
                    
                    if key == 13:  # ENTER to play
                        if self.video_url:  # Make sure URL is set
                            print(f"Starting playback of: {self.video_title}")
                            if self.play_video():
                                print("Video launched successfully")
                                self.search_mode = False
                                self.result_found = False
                                time.sleep(0.5)  # Give VLC time to start
                                cv2.destroyWindow("YouTube Search")
                            else:
                                print("Failed to launch video")
                        else:
                            print("Error: Video URL not set")
                    elif key == 27:  # ESC to search again
                        self.search_gui.result_title = None
                        self.search_gui.search_text = ""
                        self.result_found = False
                
                else:
                    # Search/Input mode
                    frame = np.zeros((self.search_gui.height, self.search_gui.width, 3), dtype=np.uint8)
                    frame = self.search_gui.draw_input_screen(frame)
                    
                    cv2.imshow("YouTube Search", frame)
                    
                    key = cv2.waitKey(100) & 0xFF
                    
                    if key == 27:  # ESC to quit
                        self.running = False
                    elif key == 13:  # ENTER to search
                        if self.search_gui.search_text.strip():
                            self.search_gui.searching = True
                            self.search_gui.result_title = None
                            search_text = self.search_gui.search_text
                            self.search_gui.search_text = ""
                            
                            # Search in background thread
                            thread = threading.Thread(target=self.search_thread, args=(search_text,))
                            thread.daemon = True
                            thread.start()
                    elif key == 8:  # Backspace to delete
                        if self.search_gui.search_text:
                            self.search_gui.search_text = self.search_gui.search_text[:-1]
                    elif key != 255 and 32 <= key <= 126:  # Regular characters
                        self.search_gui.search_text += chr(key)
            
            else:
                # Player mode
                frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
                frame = self.draw_player_screen(frame)
                
                cv2.imshow("YouTube Player", frame)
                
                key = cv2.waitKey(500) & 0xFF
                
                if key == 27:  # ESC to quit
                    self.running = False
                elif key == ord('s'):  # S to search new video
                    self.stop_video()
                    self.search_mode = True
                    self.result_found = False
                    self.video_title = None
                    self.video_url = None
                    cv2.destroyWindow("YouTube Player")
        
        self.stop_video()
        cv2.destroyAllWindows()
        print("YouTube Player closed")


if __name__ == "__main__":
    player = YouTubePlayer()
    player.run()

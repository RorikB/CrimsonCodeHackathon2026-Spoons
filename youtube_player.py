import cv2
import numpy as np
import subprocess
import os
import threading
from yt_dlp import YoutubeDL
import time

class YouTubePlayer:
    def __init__(self, width=1000, height=700):
        self.width = width
        self.height = height
        self.running = True
        self.video_url = None
        self.video_title = None
        self.video_process = None
        self.is_playing = False
        
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
        """Play the video using VLC"""
        if not self.video_url:
            return False
        
        try:
            print(f"Playing: {self.video_title}")
            # Use VLC to play the video
            vlc_path = "vlc"  # Assumes VLC is in PATH
            
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
                    vlc_found = True  # Assume it's in PATH
            
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
    
    def draw_input_screen(self, frame):
        """Draw the YouTube search/input screen"""
        cv2.rectangle(frame, (0, 0), (self.width, self.height), (20, 20, 20), -1)
        
        # Title
        cv2.putText(frame, "YOUTUBE VIDEO PLAYER", (self.width//2 - 200, 80),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 2)
        
        # Instructions
        y_pos = 200
        cv2.putText(frame, "Enter a YouTube URL or search query:", (80, y_pos),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 1)
        
        y_pos += 50
        cv2.putText(frame, "(Examples: 'Never Gonna Give You Up' or 'https://youtube.com/...')", (80, y_pos),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (150, 150, 150), 1)
        
        y_pos += 100
        cv2.putText(frame, "Type in terminal and press ENTER to search", (80, y_pos),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 200, 255), 1)
        
        y_pos += 50
        cv2.putText(frame, "Current video: " + (self.video_title[:50] if self.video_title else "None"), 
                   (80, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 255, 100), 1)
        
        y_pos += 50
        status = "▶ Playing" if self.is_playing else "⏸ Stopped"
        status_color = (0, 255, 0) if self.is_playing else (180, 180, 180)
        cv2.putText(frame, status, (80, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 2)
        
        # Instructions at bottom
        y_pos = self.height - 80
        cv2.putText(frame, "CONTROLS:", (80, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 1)
        y_pos += 35
        cv2.putText(frame, "ESC - Exit | S - Stop video", (80, y_pos), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (150, 150, 150), 1)
        
        return frame
    
    def run(self):
        """Run the YouTube player"""
        print("Starting YouTube Player...")
        print("Usage: Type a YouTube URL or search query in the terminal")
        
        while self.running:
            frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            frame = self.draw_input_screen(frame)
            
            cv2.imshow("YouTube Player", frame)
            
            key = cv2.waitKey(500) & 0xFF
            
            if key == 27:  # ESC to quit
                self.running = False
            elif key == ord('s'):  # S to stop video
                self.stop_video()
                print("Video stopped")
        
        self.stop_video()
        cv2.destroyAllWindows()
        print("YouTube Player closed")
    
    def interactive_mode(self):
        """Interactive mode for searching and playing videos"""
        print("\n=== YOUTUBE PLAYER ===")
        print("Commands:")
        print("  search <query> - Search for a video")
        print("  play - Play the current video")
        print("  stop - Stop the current video")
        print("  quit - Exit the player\n")
        
        while True:
            try:
                cmd = input("Enter command: ").strip().lower()
                
                if cmd.startswith("search "):
                    query = cmd[7:]
                    if self.search_youtube(query):
                        print(f"Found: {self.video_title}")
                    else:
                        print("Video not found")
                
                elif cmd == "play":
                    if self.video_url:
                        self.play_video()
                    else:
                        print("No video selected. Search first!")
                
                elif cmd == "stop":
                    self.stop_video()
                    print("Video stopped")
                
                elif cmd == "quit":
                    self.stop_video()
                    print("Exiting...")
                    break
                
                else:
                    print("Unknown command. Type 'search <query>', 'play', 'stop', or 'quit'")
            
            except KeyboardInterrupt:
                self.stop_video()
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    player = YouTubePlayer()
    # Use interactive mode for easier testing
    player.interactive_mode()

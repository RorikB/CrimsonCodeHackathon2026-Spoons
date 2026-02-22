"""
Google Calendar API GUI Display
================================

Shows Google Calendar events in a small GUI box on the side of the screen.
Can be placed in top-right corner like a smart mirror widget.
"""

import cv2
import numpy as np
from Calendar_Setup.google_calendar_api import GoogleCalendarAPI
from datetime import datetime

class GoogleCalendarDisplay:
    def __init__(self, width=400, height=600):
        self.width = width
        self.height = height
        self.cal = GoogleCalendarAPI()
        self.running = True
        
    def draw_calendar(self, frame):
        """Draw calendar on the frame"""
        # Draw background
        cv2.rectangle(frame, (0, 0), (self.width, self.height), (20, 20, 20), -1)
        
        # Get today's events
        today_items = self.cal.get_todays_events()
        
        # Header
        cv2.putText(frame, "TODAY", (15, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        date_str = datetime.now().strftime("%a, %b %d")
        cv2.putText(frame, date_str, (15, 55),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (150, 150, 150), 1)
        
        # Draw horizontal line
        cv2.line(frame, (10, 65), (self.width-10, 65), (100, 100, 100), 1)
        
        # Draw events
        y_offset = 85
        max_items_shown = 5
        
        if not today_items:
            cv2.putText(frame, "No events today", (15, y_offset+20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 200, 100), 1)
        else:
            for i, event in enumerate(today_items[:max_items_shown]):
                # Item title
                title = event['title']
                if len(title) > 30:
                    title = title[:27] + "..."
                
                color = (100, 200, 255)  # Light blue for events
                if event.get('all_day'):
                    color = (200, 100, 255)  # Purple for all-day
                
                cv2.putText(frame, f"{title}", (15, y_offset),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
                
                # Time
                if event.get('all_day'):
                    time_str = "All Day"
                else:
                    # Parse time from start
                    try:
                        if isinstance(event['start'], str):
                            # Format: "2026-02-21T14:30:00Z" or "2026-02-21"
                            if 'T' in event['start']:
                                time_str = event['start'].split('T')[1].split(':')[0:2]
                                time_str = f"{time_str[0]}:{time_str[1]}"
                            else:
                                time_str = "All Day"
                        else:
                            time_str = event['start'].strftime("%I:%M %p")
                    except:
                        time_str = "Time TBA"
                
                cv2.putText(frame, time_str, (20, y_offset + 18),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.45, (180, 180, 180), 1)
                
                # Separator line
                if i < len(today_items[:max_items_shown]) - 1:
                    cv2.line(frame, (15, y_offset + 28), (self.width-15, y_offset + 28),
                            (60, 60, 60), 1)
                
                y_offset += 45
        
        # Bottom info
        cv2.putText(frame, f"Total: {len(today_items)} events", (15, self.height - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 1)
        
        # # Instructions
        # cv2.putText(frame, "Press Q to quit", (15, self.height - 3),
        #            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (100, 100, 100), 1)
        
        return frame
    
    def run(self):
        """Run the calendar display"""
        print("\n🔐 Authenticating with Google Calendar...")
        
        if not self.cal.authenticate():
            print("❌ Authentication failed")
            return
        
        print("✓ Connected to Google Calendar!\n")
        
        print("📺 Calendar display running...")
        print("   Drag the window to position it (top-right recommended)")
        print("   Press 'ESC' to quit\n")
        
        while self.running:
            # Create frame
            frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            
            # Draw calendar
            frame = self.draw_calendar(frame)
            
            # Display
            cv2.imshow("Google Calendar", frame)
            
            # Handle key press (update every 1 second)
            key = cv2.waitKey(1000) & 0xFF
            
            if key == 27: # ESC key to quit:
                self.running = False
        
        cv2.destroyAllWindows()
        print("\n✓ Calendar closed")


if __name__ == "__main__":
    print("\n" + "="*50)
    print("  GOOGLE CALENDAR API - GUI DISPLAY")
    print("="*50)
    
    try:
        calendar = GoogleCalendarDisplay()
        calendar.run()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you've set up Google Calendar API:")
        print("1. Read QUICK_START_CALENDAR.txt")
        print("2. Create credentials.json in project folder")
        print("3. Run again")

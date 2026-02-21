import cv2
import numpy as np
from datetime import datetime
import time

class ClockGUI:
    def __init__(self, width=400, height=200):
        self.width = width
        self.height = height
        self.is_24_hour = False  # Default to 12-hour format
        self.running = True
        
    def get_time_string(self):
        """Get current time formatted based on 12/24 hour setting"""
        now = datetime.now()
        if self.is_24_hour:
            return now.strftime("%H:%M:%S")
        else:
            return now.strftime("%I:%M:%S %p")
    
    def draw_clock(self, frame):
        """Draw the clock display on the frame"""
        # Draw background
        cv2.rectangle(frame, (0, 0), (self.width, self.height), (20, 20, 20), -1)
        
        # Get time string
        time_str = self.get_time_string()
        
        # Draw main time display
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 2
        thickness = 2
        color = (0, 255, 0)  # Green
        
        # Get text size for centering
        text_size = cv2.getTextSize(time_str, font, font_scale, thickness)[0]
        text_x = (self.width - text_size[0]) // 2
        text_y = (self.height // 2) + (text_size[1] // 2)
        
        cv2.putText(frame, time_str, (text_x, text_y), font, font_scale, color, thickness)
        
        # Draw format indicator
        # format_text = "24H" if self.is_24_hour else "12H"
        # cv2.putText(frame, format_text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
        
        return frame
    
    def run(self):
        """Run the clock GUI"""
        while self.running:
            # Create blank frame
            frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            
            # Draw clock
            frame = self.draw_clock(frame)
            
            # Display frame
            cv2.imshow("Clock", frame)
            
            # Handle key presses (1ms timeout)
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):  # Quit
                self.running = False
            elif key == ord('t'):  # Toggle format
                self.is_24_hour = not self.is_24_hour
                print(f"Switched to {'24-hour' if self.is_24_hour else '12-hour'} format")
        
        cv2.destroyAllWindows()

if __name__ == "__main__":
    clock = ClockGUI()
    clock.run()

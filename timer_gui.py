import cv2
import numpy as np
import time
from timer import Timer

class TimerGUI:
    def __init__(self, width=400, height=300):
        self.width = width
        self.height = height
        self.timer = Timer()
        self.running = True
        
    def draw_timer(self, frame):
        """Draw the timer display on the frame"""
        # Draw background
        cv2.rectangle(frame, (0, 0), (self.width, self.height), (20, 20, 20), -1)
        
        # Get remaining time
        remaining = self.timer.get_remaining_time()
        is_active = self.timer.is_active()
        
        # Format time as MM:SS
        minutes = remaining // 60
        seconds = remaining % 60
        time_str = f"{minutes:02d}:{seconds:02d}"
        
        # Choose color based on state
        if not is_active:
            color = (100, 100, 100)  # Gray when inactive
            status_text = "Timer Inactive"
        elif remaining <= 10:
            color = (0, 0, 255)  # Red when almost done
            # status_text = "FINISHING!"
        else:
            color = (0, 255, 0)  # Green when active
            status_text = "Timer Running"
        
        # Draw time display (large in center)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 3
        thickness = 3
        
        text_size = cv2.getTextSize(time_str, font, font_scale, thickness)[0]
        text_x = (self.width - text_size[0]) // 2
        text_y = (self.height // 2) + (text_size[1] // 2)
        
        cv2.putText(frame, time_str, (text_x, text_y), font, font_scale, color, thickness)
        
        # Draw status text
        status_color = (200, 200, 200) if is_active else (100, 100, 100)
        cv2.putText(frame, status_text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 2)
        
        # Draw duration if active
        if is_active:
            duration = self.timer.get_duration()
            duration_text = f"Duration: {duration}s"
            cv2.putText(frame, duration_text, (20, self.height - 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (150, 150, 150), 1)
        
        # Draw instructions
        instructions = "Press 'Q' to quit"
        cv2.putText(frame, instructions, (20, self.height - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 100, 100), 1)
        
        return frame
    
    def run(self, duration_seconds):
        """Run the timer GUI"""
        print(f"Starting timer for {duration_seconds} seconds...")
        
        # Start the timer
        self.timer.start(duration_seconds)
        
        while self.running and self.timer.is_active():
            # Create blank frame
            frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            
            # Draw timer
            frame = self.draw_timer(frame)
            
            # Display frame
            cv2.imshow("Timer", frame)
            
            # Handle key presses (100ms timeout for smooth updates)
            key = cv2.waitKey(100) & 0xFF
            
            if key == ord('q'):
                print("Timer stopped by user")
                self.running = False
                self.timer.stop()
        
        # Timer finished
        if self.timer.is_active() == False and self.running:
            print("\n⏰ Timer finished!")
            
            # Show "Time's Up!" message
            for _ in range(30):  # Show for 3 seconds
                frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
                cv2.rectangle(frame, (0, 0), (self.width, self.height), (20, 20, 20), -1)
                
                cv2.putText(frame, "TIME'S UP!", (self.width//2 - 120, self.height//2),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 3)
                
                cv2.imshow("Timer", frame)
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
        
        cv2.destroyAllWindows()

if __name__ == "__main__":
    # Test the timer with 10 seconds
    timer_gui = TimerGUI()
    timer_gui.run(15)

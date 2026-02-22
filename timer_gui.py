import cv2
import numpy as np
import time
from timer import Timer

class TimerInputGUI:
    # hardcoded gui stuff replace with the zones instead
    def __init__(self, width=500, height=450):
        self.width = width
        self.height = height
        self.selected_duration = None
        self.custom_input = ""
        self.presets = [30, 60, 120, 300]  # 30s, 1m, 2m, 5m
        self.button_rects = []  # Store button coordinates for click detection
        self.exit_button_rect = None
        self.exit_clicked = False
        
    def mouse_callback(self, event, x, y, flags, param):
        """Handle mouse clicks on buttons"""
        if event == cv2.EVENT_LBUTTONDOWN:
            # Check preset buttons
            for i, preset in enumerate(self.presets):
                btn_x = 50 + (i % 2) * 225
                btn_y = 120 + (i // 2) * 80
                if btn_x <= x <= btn_x + 180 and btn_y <= y <= btn_y + 60:
                    self.selected_duration = preset
            
            # Check exit button
            if self.exit_button_rect:
                ex, ey = self.exit_button_rect
                if ex <= x <= ex + 100 and ey <= y <= ey + 50:
                    self.exit_clicked = True
        
    def draw_input_screen(self, frame):
        """Draw the timer input selection screen"""
        cv2.rectangle(frame, (0, 0), (self.width, self.height), (20, 20, 20), -1)
        
        # Title
        cv2.putText(frame, "SET TIMER", (self.width//2 - 100, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 2)
        
        # Preset buttons
        button_y = 120
        for i, preset in enumerate(self.presets):
            x = 50 + (i % 2) * 225
            y = button_y + (i // 2) * 80
            
            # Convert to MM:SS format
            mins = preset // 60
            secs = preset % 60
            label = f"{mins}:{secs:02d}" if mins > 0 else f"{secs}s"
            
            cv2.rectangle(frame, (x, y), (x + 180, y + 60), (100, 100, 100), 2)
            cv2.putText(frame, label, (x + 45, y + 40), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.2, (200, 200, 200), 2)
        
        # Custom input section
        cv2.putText(frame, "Or type custom (e.g., 45 or 1:30):", (50, 320), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (150, 150, 150), 1)
        cv2.rectangle(frame, (50, 340), (450, 370), (80, 80, 80), 2)
        cv2.putText(frame, self.custom_input + ("|" if len(self.custom_input) < 15 else ""), 
                   (60, 360), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (200, 200, 200), 1)
        
        # Exit button
        exit_x, exit_y = 50, 390
        self.exit_button_rect = (exit_x, exit_y)
        cv2.rectangle(frame, (exit_x, exit_y), (exit_x + 100, exit_y + 50), (0, 0, 255), 2)
        cv2.putText(frame, "EXIT", (exit_x + 25, exit_y + 35), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.9, (200, 200, 200), 2)
        
        # Instructions
        # cv2.putText(frame, "Click button, type & ENTER, or click EXIT", (160, 420), 
        #            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 100, 100), 1)
        
        return frame
    
    def run(self):
        """Run the timer input GUI"""
        cv2.namedWindow("Timer Setup")
        cv2.setMouseCallback("Timer Setup", self.mouse_callback)
        
        while True:
            frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            frame = self.draw_input_screen(frame)
            
            cv2.imshow("Timer Setup", frame)
            
            # Check if exit button was clicked
            if self.exit_clicked:
                cv2.destroyAllWindows()
                return None
            
            # Check if a preset button was clicked
            if self.selected_duration is not None:
                cv2.destroyAllWindows()
                return self.selected_duration
            
            key = cv2.waitKey(100) & 0xFF
            
            if key == 13:  # ENTER key
                if self.custom_input:
                    try:
                        if ':' in self.custom_input:
                            parts = self.custom_input.split(':')
                            minutes = int(parts[0])
                            seconds = int(parts[1])
                            duration = minutes * 60 + seconds
                        else:
                            duration = int(self.custom_input)
                        
                        if duration > 0:
                            cv2.destroyAllWindows()
                            return duration
                    except:
                        self.custom_input = ""
            
            elif key == 8:  # Backspace
                self.custom_input = self.custom_input[:-1]
            
            elif 48 <= key <= 57 or key == 58:  # 0-9 and :
                if len(self.custom_input) < 15:
                    self.custom_input += chr(key)
            
            elif key == 27:  # ESC to quit
                cv2.destroyAllWindows()
                return None


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
            status_text = "FINISHING!"
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
            
            if key == 27:  # ESC key to quit
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
                if cv2.waitKey(100) & 0xFF == 27:  # Allow exit during this time
                    break
        
        cv2.destroyAllWindows()

if __name__ == "__main__":
    input_gui = TimerInputGUI()
    duration = input_gui.run()
    
    if duration:
        timer_gui = TimerGUI()
        timer_gui.run(duration)

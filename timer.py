import time

class Timer:
    def __init__(self):
        self.start_time = None
        self.duration = None
        self.end_time = None
        self.active = False

    def start(self, duration_seconds):
        duration_seconds = float(duration_seconds)
        self.start_time = time.time()
        self.duration = duration_seconds
        self.end_time = self.start_time + duration_seconds
        self.active = True

    def stop(self):
        self.start_time = None
        self.duration = None
        self.end_time = None
        self.active = False

    def is_active(self):
        if not self.active:
            return False
        if time.time() >= self.end_time:
            self.stop()
            return False
        return True

    def get_remaining_time(self):
        if not self.is_active():
            return 0
        return max(0, int(self.end_time - time.time()))

    def get_duration(self):
        return self.duration
    
    def get_status_string(self):
        """Get current timer status as a formatted string"""
        if not self.is_active():
            return "Timer inactive"
        
        remaining = self.get_remaining_time()
        minutes = remaining // 60
        seconds = remaining % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    
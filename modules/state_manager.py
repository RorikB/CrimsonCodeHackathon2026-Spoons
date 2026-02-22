from datetime import datetime
from timer import Timer

class StateManager:
    def __init__(self):
        self.timer = Timer()
        self.state = {
            "Weather": "72°F Sunny",
            "Calendar": None,
            "Music": "No song playing",
        }

    def get(self, key, default=None):
        """Return dynamic content for zones"""
        if key == "Time":
            return datetime.now().strftime("%I:%M %p")  # 12-hour format
        elif key == "Timer":
            if self.timer.is_active():
                remaining = self.timer.get_remaining_time()
                minutes = remaining // 60
                seconds = remaining % 60
                return f"{minutes}:{seconds:02d}"
            else:
                return "0:00"
        else:
            return self.state.get(key, default)

    def update_state(self, key, value):
        """Update static state or start timer"""
        if key == "Timer":
            self.timer.start(value)
        else:
            self.state[key] = value
from clock import get_current_time
from calendar import get_next_event

def __init__(self):
    self.state = {
        "Weather": "72 degrees Fahrenheit Sunny",
        "Timer": "5:00",
        "Music": "No song playing"
    }

def get_state(self, key):
    if key == "Time":
        return get_current_time()
    elif key == "Calendar":
        return get_next_event()
    else:
        return self.state.get(key, f"{key} Placeholder")

def update_state(self,key,value):
    self.state[key] = value
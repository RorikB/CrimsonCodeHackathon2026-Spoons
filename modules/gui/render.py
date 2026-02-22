import cv2
from datetime import datetime
from .layout import get_layout_zones

def render_zones(frame, zones, state):
    for name, (x,y,w,h) in zones.items():
        # Draw rectangle
        cv2.rectangle(frame, (x,y),(x+w,y+h), (255,255,255), 2)

        # Determine what to display
        if name == "Time":
            content = datetime.now().strftime("%I:%M %p")
        else:
            content = state.get(name, f"{name} Placeholder")

        # Draw text
        cv2.putText(frame, str(content), (x+10, y+30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    return frame
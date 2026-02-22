import cv2
import numpy as np
from datetime import datetime

def render_zones(frame, zones, state):
    overlay = frame.copy()
    for zone in zones:
        x,y,w,h = int(zone.x), int(zone.y), int(zone.w), int(zone.h)
        cv2.rectangle(overlay, (x,y), (x+w, y+h), (255,255,255), 2)

        if zone.name == "Time":
            zone.content = datetime.now().strftime("%I:%M %p")
        else:
            zone.content = state.get(zone.name, f"{zone.name} Placeholder")

        cv2.putText(overlay, str(zone.content), (x+10, y+30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255), 2)

        zone.update(speed=0.1)

    cv2.addWeighted(overlay,1.0, frame, 0, 0, frame)
    return frame
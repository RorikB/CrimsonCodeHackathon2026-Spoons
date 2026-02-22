import cv2
import numpy as np
from .layout import get_layout_zones
from .render import render_zones

def fullscreen_mirror(state, focus=None):
    height, width = 1080, 1920
    frame = np.zeros((height, width, 3), dtype=np.uint8)

    zones = get_layout_zones(width, height)

    window_name = "Smart Mirror"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        frame[:] = 0 

        # adjust zone focus
        for zone in zones:
            if focus and zone.name == focus:
                zone.target_w = zone.w * 1.5
                zone.target_h = zone.h * 1.5
                zone.opacity = 1.0
            else:
                zone.target_w = zone.w
                zone.target_h = zone.h
                zone.opacity = 0.3 if focus else 1.0

        frame = render_zones(frame,zones, state)
        cv2.imshow(window_name, frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            break

        elif key == ord('w'):
            focus == "Weather"
        elif key == ord('t'):
            focus == "Time"
        elif key == ord('c'):
            focus == "Calendar"
        elif key == ord('m'):
            focus == "Music"
        elif key == ord('y'):
            focus == None
        
    cv2.destroyAllWindows()
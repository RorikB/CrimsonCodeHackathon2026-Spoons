import cv2
import numpy as np
from .layout import get_layout_zones
from .render import render_zones

def fullscreen_mirror(state):
    height, width = 1080, 1920
    frame = np.zeros((height, width, 3), dtype=np.uint8)

    window_name = "Smart Mirror"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        frame[:] = 0 
        zones = get_layout_zones(width, height)
        frame = render_zones(frame, zones, state)
        cv2.imshow(window_name, frame)

        # press q to quit
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            break
    cv2.destroyAllWindows()
from .zone import Zone

def get_layout_zones(screen_width, screen_height):
    return [
        Zone("Time", 50,50,300,100),
        Zone("Weather", screen_width - 350, 50, 300, 100),
        Zone("Calendar", 50,200,500,300),
        Zone("Timer", screen_width - 400, 200, 350, 200),
        Zone("Music", 50, screen_height - 200, 500, 150)
    ]
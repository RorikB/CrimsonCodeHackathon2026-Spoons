class Zone:
    def __init__(self, name, x, y, w, h):
        self.name = name
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.content = ""
        self.opacity = 1.0
        self.target_w = w
        self.target_h = h
    
    def update(self, speed=0.1):
        self.w += (self.target_w - self.w) * speed
        self.h += (self.target_h - self.h) * speed

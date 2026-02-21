import time

class Timer:
    def __init__(self):
        self.start_time = None
        self.duration = None
        self.end_time = None
        self.active = False

    def start(self, duration_seconds: int):
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
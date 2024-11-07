
class Timer:
    def __init__(self, time):
        self.time = time
        self.time_remaining = time

    def start(self):
        self.time_remaining = self.time
    
    def update(self, delta_time):
        self.time_remaining -= delta_time
        if self.time_remaining <= 0:
            return True
        return False
    
    def reset(self, time=None):
        if time is not None:
            self.time = time
        self.time_remaining = self.time
from time import *


class Timer:

    def __init__(self):
        self.start_time = time()
        self.stop_time = self.start_time
        self.time_passed = 0

    def stop(self):
        self.stop_time = time()
        self.time_passed = self.stop_time - self.start_time

    def reset(self):
        self.start_time = time()

    def get_time(self):
        return self.time_passed

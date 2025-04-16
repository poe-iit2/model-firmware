# This file is for demonstration, do not include in firmware 
import time

time.ticks_ms = lambda: round(time.time()*1000)
time.ticks_diff = lambda a, b: b-a

class Pin:
    def __init__(self, pin):
        self._pin = pin
    def value(self):
        return 0
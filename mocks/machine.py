# This file is for demonstration, do not include in firmware 
import time

time.ticks_ms = lambda: round(time.time()*1000)
time.ticks_diff = lambda a, b: b-a

class Pin:
    IN = 0

    def __init__(self, pin, *args):
        self._pin = pin
    def value(self):
        return 0
    
class ADC:
    def __init__(self, *args):
        pass
    def read_u16(self):
        return 0

# This file is for demonstration, do not include in firmware 

class NeoPixel:
    def __init__(self, pin, num_leds):
        self._pin = pin._pin
        self._leds = [(0,0,0) for _ in range(num_leds)]

    def __setitem__(self, idx, value):
        self._leds[idx] = value

    def write(self):
        print(self._leds)
    
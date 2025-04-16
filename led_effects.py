import network
import asyncio
import neopixel
import time
import math
import machine

leds = neopixel.NeoPixel(machine.Pin(1), 5)

def led_solid(color):
    def update(leds, t, off=0, l=0):
        for i in range(off, off+l):
            leds[i] = color
    return update

def led_pulse(color, dur=1):
    def update(leds, x, off=0, l=0):
        y = (math.sin(x * 2 * math.pi / dur) + 1) / 2
        c = (color[0] * y, color[1] * y, color[2] * y)
        for i in range(off, off+l):
            leds[i] = c
    return update

class LedSplitter:
    def __init__(self, config):
        self.config = config

    def __call__(self, leds, t, off=0, l=0):
        for f, i in self.config:
            f(leds, t, off, i)
            off += i

async def led_engine(f, l=0):
    t0 = time.ticks_ms()
    while True:
        await asyncio.sleep(0.01)
        f(leds, time.ticks_diff(t0, time.ticks_ms()) / 1000, 0, l)
        leds.write()


async def main():
    await led_engine(LedSplitter((
        (led_pulse((255, 128, 0)), 1),
        (led_solid((0, 0, 10)), 4)
        )))

asyncio.run(main())
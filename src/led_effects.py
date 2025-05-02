import asyncio
import neopixel
import time
import math
import machine

def led_sawtooth(color):
    def update(x):
        y = x % 1
        y = 1 - y
        y = y ** 1.5
        return (int(color[0] * y), int(color[1] * y), int(color[2] * y))
    return update

def led_sin(color):
    def update(x):
        y = math.sin(x * math.pi) ** 2
        return (int(color[0] * y), int(color[1] * y), int(color[2] * y))
    return update

def led_wave(f, v=1, freq=1):
    k = freq / v
    w = freq
    def update(leds, t, off=0, l=0):
        for x in range(off, off+l):
            leds[x] = f(k*x-w*t)
    return update

def led_grad(color):
    def update(leds, x, off=0, l=0):
        for i in range(l):
            y = i/l
            leds[i+off] = (int(color[0] * y), int(color[1] * y), int(color[2] * y))
    return update

def led_solid(color):
    def update(leds, t, off=0, l=0):
        for i in range(off, off+l):
            leds[i] = color
    return update

def led_pulse(color, dur=1):
    def update(leds, x, off=0, l=0):
        y = (math.sin(x * 2 * math.pi / dur) + 1) / 2
        c = (int(color[0] * y), int(color[1] * y), int(color[2] * y))
        for i in range(off, off+l):
            leds[i] = c
    return update

class Reverser:
    def __init__(self, leds, off=0, l=0):
        self.leds = leds
        self.off = off
        self.l = l
        self.c = (self.l+self.off-1)-(-self.off)

    def __setitem__(self, i, x):
        # self.leds[self.c-i+self.off] = (255,255,255)
        # for i in range(self.c-self.l, self.c):
        #     self.leds[i] = (255,255,0)
        self.leds[self.c-i] = x
        pass

    def __getitem__(self, i):
        return self.leds[self.c-i]

def reversed(f):
    def update(leds, t, off=0, l=0):
        return f(Reverser(leds, off, l), t, off, l)
    return update

class LedSegment:
    def __init__(self, config):
        self.reversed = config.get("reversed", False)
        if "color" in config:
            # self.effect = led_solid(config["color"])
            self.evac_occupied()
            # self.effect = led_grad((255,0,0))
        else:
            self.effect = led_solid((0,0,0))

    def evac_occupied(self):
        self.effect = led_wave(led_sin((0,255,10)), 7.5, 1.5)

    def evac_unoccupied(self):
        self.effect = led_solid((10, 0, 0))
        # self.effect = led_wave(led_sin((64,0,0)), 15, 0.75)

    def off(self):
        self.effect = led_solid((0,0,0))

    def safe(self):
        self.effect = led_solid((10,10,10))
    
    def __call__(self, leds, t, off=0, l=0):
        effect = self.effect
        if self.reversed:
            effect = reversed(effect)
        return effect(leds, t, off, l)

class LedChain:
    def __init__(self, config):
        self.config = []
        for c in config:
            self.config.append((neopixel.NeoPixel(machine.Pin(c["PIN"]), c["COUNT"]), c["COUNT"]))

    def __setitem__(self, i, x):
        j = 0
        for leds, n in self.config:
            if n + j > i:
                leds[i-j] = x
                return
            j += n

    def __getitem__(self, i):
        j = 0
        for leds, n in self.config:
            if n + j > i:
                return leds[i-j]
            j += n
    
    def write(self):
        for leds, _ in self.config:
            leds.write()

class LedSplitter:
    def __init__(self, config):
        self.config = config

    def __call__(self, leds, t, off=0, l=0):
        for f, i in self.config:
            f(leds, t, off, i)
            off += i

async def led_engine(leds, f, l=0):
    t0 = time.ticks_ms()
    while True:
        await asyncio.sleep(0.01)
        f(leds, time.ticks_diff(t0, time.ticks_ms()) / 1000, 0, l)
        leds.write()

def make_segments(config):
    segments = {}
    splitter_config = []
    for c in config:
        segment = LedSegment(c)
        splitter_config.append((segment, c["span"]))
        if "name" in c:
            segments[c["name"]] = segment
    return (segments, LedSplitter(splitter_config))

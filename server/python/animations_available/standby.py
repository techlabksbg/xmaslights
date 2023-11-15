from program import Program
from leds import LEDs
import colorsys
import time
import random

# Ubuntu-Linux: sudo apt install  python3-webcolors
# Windows:      pip3 install colorsys

class Standby(Program):
    def __init__(self, config):
        self.config = config
        self.led = -1
        self.start = time.time()

    def step(self, leds:LEDs, points=None) -> None:
        leds.clearTo([0,0,0])
        dt = (time.time()-self.start)/10
        if self.led==-1 or dt>1.0:
            self.led = random.randrange(leds.n)
            self.hue = random.random()
            self.start = time.time()
            dt = 0

        br = 0.1*(0.5-abs(0.5-dt))
        c : list(int,int,int) = [int(x*255) for x in colorsys.hsv_to_rgb(self.hue, 1.0, br)]
        leds.setColor(self.led, c)
        

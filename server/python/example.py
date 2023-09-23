from program import Programm
from leds import LEDs
import colorsys
import time

# Ubuntu-Linux: sudo apt install  python3-webcolors
# Windows:      pip3 install colorsys

class Example(Programm):
    def __init__(self):
        self.start = time.time()

    def step(self, leds:LEDs) -> None:
        dt = time.time()-self.start
        h = ((dt/10) % 1.0)
        for l in range(leds.n):
            c : list(int,int,int) = [int(x*255) for x in colorsys.hsv_to_rgb(h+l/leds.n,1.0,0.01)]
            leds.setColor(l, c)
        

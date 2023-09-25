from program import Programm
from leds import LEDs
import colorsys
import time

# Ubuntu-Linux: sudo apt install  python3-webcolors
# Windows:      pip3 install colorsys

class Example(Programm):
    def __init__(self):
        self.start = time.time()
        self.perdiod = 10

    def setConfig(self, config):
        if 'period' in config:
            self.period = float(config['period'])
            if (self.perdiod<1):
                self.perdiod = 1.0
            if (self.period>30):
                self.perdiod = 30.0
            print(f"New period {self.period}")
            

    def step(self, leds:LEDs) -> None:
        dt = time.time()-self.start
        h = ((dt/self.perdiod) % 1.0)
        for l in range(leds.n):
            c : list(int,int,int) = [int(x*255) for x in colorsys.hsv_to_rgb(h+l/leds.n,1.0,0.01)]
            leds.setColor(l, c)
        

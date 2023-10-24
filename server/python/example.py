from program import Program
from leds import LEDs
import colorsys
import time

# Ubuntu-Linux: sudo apt install  python3-webcolors
# Windows:      pip3 install colorsys

class Example(Program):
    def __init__(self):
        self.start = time.time()
        self.period = 3
        self.saturation = 1.0
        self.brightness = 0.02

    def setConfig(self, config):
        if 'period' in config:
            self.period = float(config['period'])
            if (self.period<0.1):
                self.period = 0.1
            if (self.period>30):
                self.period = 30.0
            print(f"New period {self.period}")

        if 'saturation' in config:
            self.saturation = float(config['saturation'])
            if self.saturation>1.0:
                self.saturation = 1.0
            if self.saturation<0.0:
                self.saturation = 0.0
        if 'brightness' in config:
            self.brightness = float(config['brightness'])
            if self.brightness>1.0:
                self.brightness = 1.0
            if self.brightness<0.0:
                self.brightness = 0.0
            

    def step(self, leds:LEDs, points=None) -> None:
        dt = time.time()-self.start
        h = ((dt/self.period) % 1.0)
        for l in range(leds.n):
            c : list(int,int,int) = [int(x*255) for x in colorsys.hsv_to_rgb(h+l/leds.n, self.saturation, self.brightness)]
            leds.setColor(l, c)
        

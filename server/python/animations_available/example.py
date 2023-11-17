from program import Program
from leds import LEDs
import colorsys
import time

# Ubuntu-Linux: sudo apt install  python3-webcolors
# Windows:      pip3 install colorsys

class Example(Program):
    def __init__(self, config):
        self.config = config
        self.start = time.time()

    def step(self, leds:LEDs, points=None) -> None:
        dt = time.time()-self.start
        h = ((dt/self.config['period']) % 1.0)
        for l in range(leds.n):
            c : list(int,int,int) = [int(x*255) for x in colorsys.hsv_to_rgb(h+l/leds.n, self.config['saturation'], self.config['brightness'])]
            leds.setColor(l, c)
        

    def defaults(self):
        return {'params':{'brightness':0.1, 
                          'saturation':1.0, 
                          'period':10},
                'autoPlay':True,
                'playFor':20,
                'web':True}
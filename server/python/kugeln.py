from program import Program

import time
import colorsys
import numpy as np

class Kugeln(Program):
    def __init__(self, config):
        self.config = config
        self.start = time.time()
       
    def step(self, leds, points):
        dt = (time.time()-self.start)/self.config['period']
        
        
        for l in range(leds.n):
            c = self.config['color']
            leds.setColor(l, c)
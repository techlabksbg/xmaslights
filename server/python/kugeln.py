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

        r = 30
        x = dt%1
        h = 150-r
        f = -4*h*x**2+4*h*x+r
        kugel = [0, 0, f]
        b = [255, 0, 0]

        
        


        for l in range(leds.n):
            x = points[0][l]
            y = points[1][l]
            z = points[2][l]
            vx = kugel[0]-x
            vy = kugel[1]-y
            vz = kugel[2]-z
            v = (vx*vx + vy*vy + vz*vz)**0.5
            if v < r:
                c = self.config['color']
            else:
                c = b
            
            leds.setColor(l, c)

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
        b = [2, 1, 0]
        for l in range(leds.n):
            v = np.linalg.norm(points[:,l]-kugel)
            if v < r:
                c = self.config['color']
            else:
                c = b
            
            leds.setColor(l, c)


    def defaults(self):
        return {'params':{'color':'040506', 
                          'period':3},
                'autoPlay':True,
                'playFor':20,
                'web':True}
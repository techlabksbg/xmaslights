from program import Program
import math
import time
import colorsys
import numpy as np


class Spiral(Program):
    def __init__(self, config):
        self.config = config
        self.start = time.time()
       
    def step(self, leds, points):
        dt = (time.time()-self.start)/self.config['period']

        a = 8
        x = dt/2
        u = ((2-2*x/(a*2*math.pi))/4*math.sin(x))
        f = ((2-2*x/(a*2*math.pi))/4*math.cos(x))
        o = ((2*x/(a*2*math.pi)))
        spiral = [u, f, o]
        b = [250,0,0]
        r = 0
        


        for l in range(leds.n):
            #x = points[0][l]
            #y = points[1][l]
            #z = points[2][l]
            #vx = kugel[0]-x
            #vy = kugel[1]-y
            #vz = kugel[2]-z
            #v = (vx*vx + vy*vy + vz*vz)**0.5
            # Same thing with numpy
            v = np.linalg.norm(points[:,l]-spiral)
            if v < r:
                c = self.config['color']
            else:
                c = b
            
            leds.setColor(l, c)

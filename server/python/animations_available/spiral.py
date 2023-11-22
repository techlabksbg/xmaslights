from program import Program
import math
import time
import colorsys
import numpy as np


class spiral(Program):
    def __init__(self, config):
        self.config = config
        self.start = time.time()
       
    def step(self, leds, points):
        t = time.time()-self.start
        # Variablennamen treffender wählen, z.B. auch
        # mehr als ein Buchstabe!
        # r für Radius, x,y für Koordinaten, t für Zeit ist ok.
        # Evtl. w für Winkel, aber besser alpha.
        a = 8
        b = [int(255*self.config['brightness']),0,0]
        d = [0,int(255*self.config['brightness']),0]
        r = 25
        y = a*2*math.pi
        x = 3*t % y 

        u = ((2-200*(x)/(y))/4*math.sin(x))
        f = ((2-200*(x)/(y))/4*math.cos(x))
        o = ((200*(x)/(y)))
        spiral = [u, f, o]
        for l in range(leds.n):
            v = np.linalg.norm(points[:,l]-spiral)
            if v < r: 
                c = d

            else:
                c = b
                
            leds.setColor(l, c)
        

    def defaults(self):
        return {'params':{'brightness':0.2},
                'autoPlay':True,
                'playFor':20,
                'web':True
                }
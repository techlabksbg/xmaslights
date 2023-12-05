from program import Program
import math
import time
import colorsys
import numpy as np


class spiral(Program):
    def __init__(self, config):
        self.config = config
        self.start = time.time()
        self.config.registerKey('umdrehungen', {'default':8, 'low':1, 'high':20, 'type':float})   

    def step(self, leds, points):
        t = time.time()-self.start
        # Variablennamen treffender wählen, z.B. auch
        # mehr als ein Buchstabe!
        # r für Radius, x,y für Koordinaten, t für Zeit ist ok.
        # Evtl. w für Winkel, aber besser alpha.
        Umdrehungen = self.config['umdrehungen']
        b = [int(rgb*self.config['brightness']) for rgb in self.config['color']]
        d = [int(rgb*self.config['brightness']) for rgb in self.config['color2']]
        r = 25
        beta = Umdrehungen*2*math.pi
        alpha = Umdrehungen/2*t % beta 

        x = ((2-200*(alpha)/(beta))/4*math.sin(alpha))
        y = ((2-200*(alpha)/(beta))/4*math.cos(alpha))
        z = ((200*(alpha)/(beta)))
        spiral = [x, y, z]
        for l in range(leds.n):
            v = np.linalg.norm(points[:,l]-spiral)
            if v < r: 
                c = d

            else:
                c = b
                
            leds.setColor(l, c)
        

    def defaults(self):
        return {'params':{'brightness':0.2,
                          'umdrehungen':8,
                          'color':[255,0,0],
                          'color2':[0,255,0]},
                'autoPlay':True,
                'playFor':45,
                'web':True
                }
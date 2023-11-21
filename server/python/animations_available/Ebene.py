from program import Program
import time
import colorsys
import numpy as np
import math

class Ebene(Program):
    def __init__(self, config):
        self.config = config
        self.start = time.time()
        self.config.registerKey('dir', {'array':True, 'len':3, 'low':-1, 'high':1, 'default':[0,0,1], 'type':float})
        self.config.registerKey('scale', {'default':100, 'low':5, 'high':500, 'type':float})

    def step(self, leds, points):
        dt = (time.time()-self.start)/self.config['period']
        
        hues = np.matmul(np.array([math.cos(dt), math.sin(dt), 0]), points)/self.config['scale']+(1-dt%1)
        for l in range(leds.n):
            h = hues[l] % 1
            c : list(int,int,int) = [int(x*255) for x in colorsys.hsv_to_rgb(h, self.config['saturation'], self.config['brightness'])]
            leds.setColor(l, c)

    def defaults(self):
        return {'params':{'brightness':0.1, 
                          'saturation':1.0, 
                          'scale':100},
                'autoPlay':True,
                'playFor':20,
                'web':True}

    def LED(position,farbe):
        by=120
        ey=[e1,e2,e3,e4]
        e1=0
        e2=by*1/4
        e3=by*2/4
        e4=by*3/4

        for l in range(l):
            if [1][l] < e4:
                if [1][l] < e3:
                    if [1][l] < e2:
                        if [1][l] < e1:
                            c = [255,255,0]
                        else: c = [255,255,255]
                    else: c = [255,255,0]
                else: c = [255,255,255]
        
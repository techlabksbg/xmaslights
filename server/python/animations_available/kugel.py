from program import Program

import time
import colorsys
import numpy as np

class Kugel(Program):
    def __init__(self, config):
        self.config = config
        self.start = time.time()
       
    def step(self, leds, points):
        dt = (time.time()-self.start)/self.config['period']

        #Radius der kugel
        r = 30
        x = dt%1
        h = 200-2*r

        #Momentane Höhe
        f = -4*h*x**2+4*h*x+r
        kugel = [0, 0, f]
        b = [125, 125, 125]
        hue = (f-r)/h
        
        


        for l in range(leds.n):
            #x = points[0][l]
            #y = points[1][l]
            #z = points[2][l]
            #vx = kugel[0]-x
            #vy = kugel[1]-y
            #vz = kugel[2]-z
            #v = (vx*vx + vy*vy + vz*vz)**0.5
            # Same thing with numpy
            v = np.linalg.norm(points[:,l]-kugel)
            if v < r:
                # c = self.config['color']
                c = [int(x*255) for x in colorsys.hsv_to_rgb(hue, self.config['saturation'], self.config['brightness'])]

            else:
                c = b
            
            leds.setColor(l, c)



    def defaults(self):
        return {'params':{'brightness':0.2, 
                          'saturation':0.2, 
                          'period':3},
                'autoPlay':False,
                'playFor': 30,
                'web':False}
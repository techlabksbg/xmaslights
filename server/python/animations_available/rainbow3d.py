from program import Program
import time
import colorsys
import numpy as np

class Rainbow3d(Program):
    def __init__(self, config):
        self.config = config
        self.start = time.time()
        self.config.registerKey('dir', {'array':True, 'len':3, 'low':-1, 'high':1, 'default':[0,0,1], 'type':float})
        self.config.registerKey('scale', {'default':100, 'low':5, 'high':500, 'type':float})

    def step(self, leds, points):
        dt = (time.time()-self.start)/self.config['period']
        
        hues = np.matmul(np.array(self.config['dir']), points)/self.config['scale']+(1-dt%1)
        for l in range(leds.n):
            h = hues[l] % 1
            c : list(int,int,int) = [int(x*255) for x in colorsys.hsv_to_rgb(h, self.config['saturation'], self.config['brightness'])]
            leds.setColor(l, c)


    def defaults(self):
        return {'params':{'brightness':0.1, 
                          'saturation':1.0, 
                          'period':10,
                          'dir':'0,0,1',
                          'scale':100},
                'autoplay':20}
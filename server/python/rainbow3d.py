from program import Program
import time
import colorsys

class Rainbow3d(Program):
    def __init__(self):
        self.start = time.time()
        self.period = 5

    def step(self, leds, points):
        dt = (time.time()-self.start)/self.period
        for l in range(leds.n):
            h = (points[2][l]/100+dt)%1
            c : list(int,int,int) = [int(x*255) for x in colorsys.hsv_to_rgb(h,1.0,1)]
            leds.setColor(l, c)

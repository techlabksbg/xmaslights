from program import Program
import time
import colorsys
import numpy as np

class Rainbow3d(Program):
    def __init__(self):
        self.start = time.time()
        self.period = 5
        self.saturation = 1.0
        self.dir = np.array([-0.1,0,-1])
        self.brightness = 1.0
        self.scale = 100

    def step(self, leds, points):
        dt = (time.time()-self.start)/self.period
        hues = np.matmul(self.dir, points)/self.scale+dt
        for l in range(leds.n):
            h = hues[l] % 1
            c : list(int,int,int) = [int(x*255) for x in colorsys.hsv_to_rgb(h, self.saturation, self.brightness)]
            leds.setColor(l, c)


    def setConfig(self, config: dict) -> None:
        if 'period' in config:
            self.period = float(config['period'])
            if (self.period<0.1):
                self.period = 0.1
            if (self.period>30):
                self.period = 30.0
            print(f"New period {self.period}")

        if 'saturation' in config:
            self.saturation = float(config['saturation'])
            if self.saturation>1.0:
                self.saturation = 1.0
            if self.saturation<0.0:
                self.saturation = 0.0
        if 'brightness' in config:
            self.brightness = float(config['brightness'])
            if self.brightness>1.0:
                self.brightness = 1.0
            if self.brightness<0.0:
                self.brightness = 0.0
            
        if 'dir' in config:
            dir = [float(x) for x in config['direction'].split(",")]
            if len(dir)==3:
                dir = np.array(dir)
                if (np.linalg.norm(dir)>0):
                    dir /= np.linalg.norm(dir)
                    self.dir = dir

        if 'scale' in config:
            self.scale = float(config['scale'])
            if (self.scale>500):
                self.scale=500
            if (self.scale<10):
                self.scale = 10


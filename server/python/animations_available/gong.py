from program import Program
import time
import colorsys
import numpy as np

class Gong(Program):
    def __init__(self, config):
        self.config = config
        self.notes = [[0,0], [0.5,4], [1.0, 3], [1.5, 2], [2,0],
                      [3,0], [3.5, 2], [4,4],[4.5,3], [10,0]]
        self.numNotes = 5
        self.bottom = 40
        self.top = 180
        self.reset()
        gongtime = [[7,40], [8,25], [8,34], [9,19], [9,28],[10,13],[10,30],[11,15],[11,24], [12,9],
                    [12,14],[12,59],[13,4],[13,49],[13,55],[14,40],[14,49],[15,34],[15,43],[16,28],
                    [16,33], [17,18], [17,23],[18,8], [10,20]]
        for t in gongtime:
            self.config.timeControl.atTime(t[0], t[1], "Gong")


    def reset(self):
        self.nextNote = 0
        self.start = time.time()

    def step(self, leds, points):
        dt = (time.time()-self.start)
        if (dt>self.notes[-1][0]):
            self.reset()
            leds.clearTo([0,0,0])
            dt = 0


        if (dt>=self.notes[self.nextNote][0]):
            note = self.notes[self.nextNote][1]
            self.nextNote+=1
            hue = note/self.numNotes
            dh =  (self.top-self.bottom)/self.numNotes
            bottom = dh*note+self.bottom
            top = bottom+dh
            for l in range(leds.n):
                if (points[2,l]>=bottom and points[2,l]<=top):
                    c : list(int,int,int) = [int(x*255) for x in colorsys.hsv_to_rgb(hue, 1.0, 1.0)]
                    leds.setColor(l, c)

        for l in range(leds.n):
            c = [int(x*0.9) for x in leds.getColor(l)]
            leds.setColor(l, c)


    def defaults(self):
        return {'params':{'brightness':0.8, 
                          'saturation':1.0},
                'autoPlay':False,
                'playFor':8,
                }
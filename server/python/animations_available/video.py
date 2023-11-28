from program import Program
from leds import LEDs
import colorsys
import time
import cv2


# Import von YouTube ist kaum möglich. Das muss direkt von einer Datei geschehen.
# Vorschlag: Neues Verzeichnis 'video', das in .gitignore eingetragen wird.
# Die Videos dort drin platzieren, schlau benennen und auf den Server kopieren.


# For Unicode one could use this workaround...
# https://stackoverflow.com/questions/71962098/python-opencv-puttext-show-non-ascii-unicode-utf-character-symbols

class Viedo(Program):
    def __init__(self, config):
        self.config = config
        self.config.registerKey('video', {'default':"NeverGonaGive.avi", 'minlen':3, 'maxlen':100, 'type':str})
        self.bbox = False
        self.initVideo()


    def initVideo(self):
        self.cap = cv2.VideoCapture("videos/"+self.config['video'])
        

    #computes the transform from LED-Coordinates (y/z) to image coordinates (w,h)
    def computeTransform(self):
        if self.bbox:
            self.scale = self.height/(self.bbox[3]-self.bbox[1])
            self.offset_h = self.scale*self.bbox[3]
            self.offset_w = -self.scale*self.bbox[2]
            self.dy = self.width-(self.scale*self.bbox[0]+self.offset_w)

    #asigns values to LEDs
    def step(self,leds,points):
        resize = cv2.resize(self.cap.read, (300, 300), interpolation = cv2.INTER_LINEAR) 
        for l in range(leds.n):
            py = points[1,l]
            pz = points[2,l]
            w = int(self.scale*py+self.offset_w+dy)
            h = int(-self.scale*pz+self.offset_h)
            if w >=0 and h >=0 and w < 300 and h < 300:
                v = (resize[w, h])
                LEDs.setColor(l, v)
        

    def defaults(self):
        return {'params':{'brightness':0.1, 
                          'saturation':1.0,},
                'autoPlay':True,
                'playFor':40,
                'web':True}
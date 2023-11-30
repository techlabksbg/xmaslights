from program import Program
from leds import LEDs
import colorsys
import time
import cv2
import numpy as np


# Import von YouTube ist kaum möglich. Das muss direkt von einer Datei geschehen.
# Vorschlag: Neues Verzeichnis 'video', das in .gitignore eingetragen wird.
# Die Videos dort drin platzieren, schlau benennen und auf den Server kopieren.


# For Unicode one could use this workaround...
# https://stackoverflow.com/questions/71962098/python-opencv-puttext-show-non-ascii-unicode-utf-character-symbols

class Video(Program):
    def __init__(self, config):
        self.config = config
        self.config.registerKey('video', {'default':"NeverGonaGive.avi", 'minlen':3, 'maxlen':100, 'type':str})
        self.bbox = False
        self.height = 300
        self.width = 300
        self.initVideo()


    def initVideo(self):
        self.cap = cv2.VideoCapture("videos/"+self.config['video'])
        


    #asigns values to LEDs
    def step(self,leds,points):
        ok, img = self.cap.read()
        if not ok:
            self.cap.release()
            self.initVideo()
            return
        resize = cv2.resize(img, (200, 200), interpolation = cv2.INTER_LINEAR) 
        for l in range(leds.n):
            py = points[1,l]
            pz = points[2,l]
            #w = int(self.scale*py+self.offset_w+self.dy)
            #h = int(-self.scale*pz+self.offset_h)
            h = int(py + 100)
            w = int(200-pz)
            if w >=0 and h >=0 and w < 300 and h < 300:
                v = resize[w, h]
                v = [int(float(rgb)*rgb/255*self.config['brightness']) for rgb in v]
                v.reverse()
                leds.setColor(l, v)
        

    def defaults(self):
        return {'params':{'brightness':0.5},
                'autoPlay':True,
                'playFor':40,
                'web':True}
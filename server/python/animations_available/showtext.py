from program import Program
from leds import LEDs
import colorsys
import time
import cv2
import numpy as np


# For Unicode one could use this workaround...
# https://stackoverflow.com/questions/71962098/python-opencv-puttext-show-non-ascii-unicode-utf-character-symbols

class ShowText(Program):
    def __init__(self, config):
        self.config = config
        self.config.registerKey('text', {'default':"Frohe Adventszeit", 'minlen':3, 'maxlen':50, 'type':str})
        self.bbox = False
        self.initText()


    def initText(self):
        self.text = self.config['text']
        bordertop = 20
        borderbottom = 15
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1
        thickness = 1

        letter_width = [cv2.getTextSize(c, font, fontScale, thickness)[0][0] for c in self.text]
        self.width = sum(letter_width)
        self.height = cv2.getTextSize(self.text, font, fontScale, thickness)[0][1]
        self.height += bordertop+borderbottom
        # print(f"Creating image of size {self.width}x{self.height} for text {self.text}")
        self.image = np.ones((self.height,self.width,3), np.uint8)
        # put single letters, with different color numbers, and variable kerning
        x = 0
        for i in range(len(self.text)):
            h = (i*0.05*10**0.5)%1
            c = [int(x*255) for x in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
            self.image = cv2.putText(self.image, self.text[i], (x,int(self.height-borderbottom)), font, fontScale, c, thickness, cv2.LINE_AA)
            x+=letter_width[i]
        self.start = time.time()
        self.computeTransform()

    #computes the transform from LED-Coordinates (y/z) to image coordinates (w,h)
    def computeTransform(self):
        if self.bbox:
            self.scale = self.height/(self.bbox[3]-self.bbox[1])
            self.offset_h = self.scale*self.bbox[3]
            self.offset_w = -self.scale*self.bbox[2]
            self.dy = self.width-(self.scale*self.bbox[0]+self.offset_w)


    def step(self, leds:LEDs, points=None) -> None:
        if self.text != self.config['text']:
            self.initText()
        if not self.bbox:
            self.bbox = [np.min(points[1,:]), np.min(points[2,:]), np.max(points[1,:]), np.max(points[2,:])]
            self.computeTransform()

        dt = (time.time()-self.start)/(self.config['period']*len(self.text)/5) % 1
        dy = self.dy*dt

        for l in range(leds.n):
            py = points[1,l]
            pz = points[2,l]
            w = int(self.scale*py+self.offset_w+dy)
            h = int(-self.scale*pz+self.offset_h)
            #if (l==0):
            #    print(f"w/h = {w}/{h}")
            if w>=0 and w<self.width and h>=0 and h<self.height:
                c = self.image[h,w]
                if sum(c)>3:
                    c = [int(cc*self.config['brightness']) for cc in c]
                else:
                    c = [1,1,1]
            else:
                c = [1,1,1]
            leds.setColor(l, c)
        

    def defaults(self):
        return {'params':{'brightness':0.3, 
                          'period':6,
                          'text':"Frohe Adventszeit"},
                'autoPlay':True,
                'playFor':40,
                'web':True}
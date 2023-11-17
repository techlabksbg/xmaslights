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
        self.bbox = False
        self.initText("Frohe Adventszeit!")


    def initText(self, text):
        maxlen = 50
        if len(text)>maxlen:
            text = text[0:maxlen]

        self.text = text
        bordertop = 20
        borderbottom = 10
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1
        thickness = 2
        color=[255]  # White, use as mask
        size, _ = cv2.getTextSize(self.text, font, fontScale, thickness)        
        self.width, self.height = size
        self.height += bordertop+borderbottom
        print(f"Creating image of size {self.width}x{self.height} for text {text}")
        self.image = np.zeros((self.height,self.width,1), np.uint8)+5
        self.image = cv2.putText(self.image, self.text, (0,int(self.height-borderbottom)), font, fontScale, color, thickness, cv2.LINE_AA)       
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
                c = self.image[h,w][0]
                if c>127:
                    h = w/100
                    c : list(int,int,int) = [int(x*255) for x in colorsys.hsv_to_rgb(h, self.config['saturation'], self.config['brightness'])]
                else:
                    c = [1,1,1]
                
            else:
                c = [1,1,1]
            leds.setColor(l, c)
        

    def defaults(self):
        return {'params':{'brightness':0.1, 
                          'saturation':1.0, 
                          'period':10},
                'autoPlay':True,
                'playFor':40}
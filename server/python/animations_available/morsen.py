from program import Program
from random import random
import time
import colorsys
from logger import logger

class Morsen(Program):
    def __init__(self, config):
        super().__init__(config)
        self.hasWord = False

    def curColor(self):
        t = (time.time()-self.startTime)/self.duration
        i = 1-abs(0.5-t)*2
        if self.code[self.position]==" " or self.code[self.position]=="|":
            self.color = [1,1,1]
        else:
            self.color = [int(x*255) for x in colorsys.hsv_to_rgb(self.hue, 1.0, i*self.config['brightness'])]

    def setNext(self):
        char = self.code[self.position]
        self.startTime = time.time()
        self.duration = self.config['period']/20*self.durations[char]
        self.next = self.startTime+self.duration
        if char==" ":
            self.hue = random()

    def newWord(self):
        self.hasWord = True
        morsecode = [ '.-', '-...', '-.-.', '-..', '.', '..-.', '--.', '....', '..', '.---', '-.-', '.-..', '--', '-.', '---', '.--.', '--.-', '.-.', '...', '-', '..-', '...-', '.--', '-..-', '-.--', '--..' ]
        morsecode = [ "|".join([c for c in code]) for code in morsecode]
        self.text = self.config['text']
        if (len(self.text)==0):
            self.text = "TECHLAB"
        self.code = " ".join([morsecode[ord(c)-65] for c in self.config['text'].upper() if ord(c)>=ord('A') and ord(c)<=ord('Z')])+"  "
        self.durations = {'.':1, '-':3, ' ':3, '|':1}
        self.start = time.time()
        self.position = 0
        self.curChar = self.code[0]
        self.hue = random()
        self.setNext()


    def step(self, leds, points):
        if (not self.hasWord):
            self.newWord()
        if self.text!=self.config['text']:
            self.newWord()
        if (time.time()>self.next):
            self.position+=1
            if (self.position>=len(self.code)):
                self.newWord()
            self.setNext()
        self.curColor()
        for l in range(leds.n):
            leds.setColor(l, self.color)




    def defaults(self):
        return {'params':{'brightness':1, 'saturation':1.0, 'period':5, 'text':'xmas'},
                'web':True,
                'autoPlay': True,
                'playFor': 20
                }
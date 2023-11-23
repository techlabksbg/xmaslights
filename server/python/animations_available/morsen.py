from program import Program
from random import random
import time
import colorsys

class Morsen(Program):
    def __init__(self, config):
        super().__init__(config)

    def curColor(self):
        [int(x*255) for x in colorsys.hsv_to_rgb(self.hue, 1.0, 1.0)]

    def setNext(self, char):
        self.next = time.time()+self.config['period']/10*self.durations[char]

    def newWord(self):
        morsecode = [ '.-', '-...', '-.-.', '-..', '.', '..-.', '--.', '....', '..', '.---', '-.-', '.-..', '--', '-.', '---', '.--.', '--.-', '.-.', '...', '-', '..-', '...-', '.--', '-..-', '-.--', '--..' ]
        self.text = self.config['text']
        if (len(self.text)==0):
            self.text = "TECHLAB"
        self.code = [morsecode[ord(c)-65] for c in self.config['text'].upper() if ord(c)>=ord('A') and ord(c)<='Z'].join(" ")
        self.durations = {'.':1, '-':3, ' ':3}
        self.start = time.time()
        self.position = 0
        self.curChar = self.code[0]
        self.hue = random()
        self.setNext()


    def step(self, leds, points):

        pass

    def defaults(self):
        return {'params':{'brightness':0.1, 'saturation':1.0, 'period':10}}
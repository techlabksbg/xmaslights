from program import Program
import time
import colorsys
import numpy as np
import math



class Ebene(Program):
    def __init__(self, config): # wird einmal aufgerufen, danach nie mehr, wird festgelegt, was ich am Programm benötige
        self.config = config
        self.start = time.time()

    def step(self, leds, points): # wird immer wieder aufgerufen, wie der Baum aussieht
        dt = (time.time()-self.start)/self.config['period']
        
        hues = np.matmul(np.array([math.cos(dt), math.sin(dt), 0]), points) # Farbenberechnung, Entfernung aller Punke der drehenden Ebene
        for l in range(leds.n):
            x = - 60
            i = 0       # Überwachung der Anzahl schleifendurchläufe
            while x <60:
                i = i + 1
                if hues[l] < x: # Setzen der Farbe an jedem zweiten Durchlauf
                    if i%2 == 0:
                        c = [int(255*self.config["brightness"]),0,0]
                    else:
                        c = [0,int(255*self.config["brightness"]),0]
                    break
                x = x + 120/8
            leds.setColor(l, c) # Festlegung der Farbe
        
    def defaults(self):
        return {'params':{'brightness':0.2,
                          'period':3,
#                          'color':"ff0000"},  # Das hat im Moment noch keinen Effekt, diese Farbe (und gleich auch noch color2 in Zeilen 25 und 27 einbauen!
                'autoPlay':True,
                'playFor': 3000, # Wie lange sollte mein Programm laufen, bevor es wechselt (in Sekunden)?
                'web':True}


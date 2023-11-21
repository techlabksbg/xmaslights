from program import Program

import time
import colorsys
import numpy as np

class Kugeln(Program):
    def __init__(self, config):
        self.config = config
        self.start = time.time()
       
    def step(self, leds, points):
        dt = (time.time()-self.start)/self.config['period']

        #Radius von Kugeln
        r1 = 30
        r2 = 10
        r3 = 5
        r = [r1, r2, r3]

        x = dt%1

        #Maximale Höhe von Kugeln
        h1 = 150-r1
        h2 = 30
        h3 = 70
        h = [h1, h2, h3]

        #Funktion von Kugeln, welche momentane Höhe ausrechnet für alle drei Kugeln 
        f = [-4*h[i]*x**2+4*h[i]*x+r[i] for i in range (3)]
        #f = [x, x, x]

        #Position der Kugeln
        kugel = [[0,0,0], [0,30,50], [0,0,60]]
        # Standart Farbe der LED's
        b = [10, 10, 10]
        

        hue = [(f[i]-r[i])/h[i] for i in range (3)]
        # hue = [x,x,x]
        
        #Anzahl der Kugeln in welche sich 1 LED befindet
        anzahl = 0
        farbe = np.array(x[0,0,0])
        for l in range(3):
            #Schaut ob ein Punkt sich innerhalb einer Kugel befindet 
            v = np.linalg.norm(points[:,l]-kugel)

        
            if anzahl 3:
                for l in range(3):
                    if 
            if v < r[l]:
                anzahl=anzahl+1
                farbe += hue[l]
                # np.array(farbe[l])
        if anzahl>0:
            c = farbe/anzahl
        else:
            c = b
        
        #Überprüfe alle zahlen, 
            #falls sie zwischen 0 - 0.24 oder 0.75 - 1, dann füge pro Zahl 1 hinzu
        #Falls der Rest gerade ist (aka. der rest ist 0) dann:
            #Für jede Zahl, überprüfe ob sie kleiner als 5 ist
                #wenn ja, dann mach nix
                #sonst, rechne -10 + die Zahl
            #Rechne die Zahlen zusammen, teile sie durch 3
            #Falls die errechnete Zahl kleiner als 0
                # 10+ errechnete Zahl (welche im minus sein muss)
                # Sonst mache nix
            #c = -^
        # Sonst
            #Rechne alle Zahlen zusammen, teile sie durch 3



        


        leds.setColor(l, c)
            
        # for l in range(leds.n):
        #     #x = points[0][l]
        #     #y = points[1][l]
        #     #z = points[2][l]
        #     #vx = kugel[0]-x
        #     #vy = kugel[1]-y
        #     #vz = kugel[2]-z
        #     #v = (vx*vx + vy*vy + vz*vz)**0.5
        #     # Same thing with numpy
        #     v = np.linalg.norm(points[:,l]-kugel)
        #     if v < r:
        #         c = self.config['color']
        #     else:
        #         c = b
            
        #     leds.setColor(l, c)
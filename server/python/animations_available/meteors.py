from program import Program
import time
import colorsys
import numpy as np
import random
import math

class Meteors(Program):
    def __init__(self, config):
        self.config = config
        self.start = time.time()
        self.newMeteor()

    # a,b must be vector like np.array([1,2,3])
    def distFromSegement(self, a,b, points):
        # Geradengleichung OA + t AB
        # Parameter für Fusspunkt: t = (AP . AB)/AB^2 
        ab = b-a
        abl = np.linalg.norm(ab)
        abl2 = abl*abl
        abinv = ab/abl2
        # Vektor aller Parameter t
        t = np.matmul(abinv, points)-np.dot(abinv,a)
        # Fusspunkte (werden nicht gebraucht, schneller geht es via Pythagoras im Dreieck APF, da die Distanzen AP sowieso gebraucht werden)
        # f = np.matmul(ab.reshape(3,1),t.reshape(1,n))+a.reshape(3,1)

        # Distanzen von A und von B
        apl = np.linalg.norm(points-a.reshape(3,1), axis=0)
        bpl = np.linalg.norm(points-b.reshape(3,1), axis=0)
        # Distanzen P zu AB
        d = np.sqrt(apl*apl-t*t*abl2)
        
        # Fusspunktparameter, Distanzen zur Geraden, Distanzen zu A und zu B
        return t,d,apl,bpl

    def meteor(self, a,b, r, points):
        n = points.shape[1]
        t,d,apl, bpl = self.distFromSegement(a,b,points)
        intensity = []
        for i in range(n):
            if t[i]<=0:
                intensity.append([0 if apl[i]>r else (r-apl[i])/r, 0.0])
            elif t[i]<=1:
                rr=r*(1-t[i])
                intensity.append([0 if d[i]>rr else (rr-d[i])/r,t[i]])
            else:
                intensity.append([0,0])

        return intensity
    
    def newMeteor(self):
        targetr = random.random()*20+30
        angle = random.random()*math.pi*2
        originr = random.random()*50+30
        self.target = np.array([math.cos(angle)*targetr, math.sin(angle)*targetr, 60])
        angle += random.random()-random.random()
        self.origin = np.array([-math.cos(angle)*originr, -math.sin(angle)*originr, 160])
        self.vector = self.target-self.origin
        self.hue = random.random()


    def step(self, leds, points):
        dt = (time.time()-self.start)/self.config['period']
        if (dt>1):
            dt = 0
            self.start =time.time()
            self.newMeteor()
        a = self.origin + 2*dt*self.vector + np.array([0,0,-dt*dt*80])
        b = a-self.vector+ np.array([0,0,-dt*dt*50])
        colorinfo = self.meteor(a,b,20,points)
        for l in range(leds.n):
            h = (self.hue+colorinfo[l][1]*0.2)%1
            bright = self.config['brightness']*colorinfo[l][0]*colorinfo[l][0]
            c : list(int,int,int) = [int(x*255) for x in colorsys.hsv_to_rgb(h, self.config['saturation'], bright)]
            if c==[0,0,0]:
                c=[1,1,1]
            leds.setColor(l, c)


    def defaults(self):
        return {'params':{'brightness':1.0, 
                          'saturation':1.0, 
                          'period':3},
                'autoPlay':True,
                'playFor': 30,
                'web':True}
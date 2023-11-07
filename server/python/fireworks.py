from program import Program
import time
import math
import colorsys
import numpy as np

class Fireworks(Program):
    def __init__(self, config):
        self.config = config
        self.start = time.time()
        self.r = 15
        self.g = 9.81
        self.c = 150
        self.col = [255, 0, 0]
        self.particles = []

    def xyz(self, time, particle): # returns x,y,z coordinates of particle at time
        z = particle['z0'] + particle['v0']*math.sin(particle['theta'])*time - 0.5*self.g*time**2
        y = particle['y0'] + particle['v0']*math.cos(particle['theta'])*math.cos(particle['phi'])*time
        x = particle['x0'] + particle['v0']*math.cos(particle['theta'])*math.sin(particle['phi'])*time
        return x,y,z
    
    def get_particles(self, sphere): # sets self.particles to list of evenly distributed particles around sphere
        num_particles = 100

        phi = math.pi * (math.sqrt(5.) - 1.)  # golden angle in radians
        points = []

        for i in range(num_particles):
            y = 1 - (i / float(num_particles - 1)) * 2  # y goes from 1 to -1
            y *= self.r  # scale y

            theta = phi * i  # golden angle increment

            x = math.cos(theta) * self.r
            z = math.sin(theta) * self.r

            points.append([x, y, z])

        for p in points:
            x = sphere[0]+p[0]
            y = sphere[1]+p[1]
            z = sphere[2]+p[2]

            theta = math.atan2(y, x)
            phi = math.atan2(math.sqrt(x**2+z**2), y)

            self.particles.append({'x0':x, 'y0':y, 'z0':z, 'theta':theta, 'phi':phi, 'v0':10, 'color':self.col})
        

    def step(self, leds, points):

        dt = (time.time()-self.start)/self.config['period']
        z = min(points[2])+dt*self.c
        firework = [0, 0, z]

        if (z > max(points[2])-2*self.r):
            self.start = time.time()
            
            self.particles = []
            self.get_particles(firework)
            
            dt = 0
            z = min(points[2])
            firework = [0, 0, z]

            self.col = [self.col[2]]+self.col[:2]
            # explode firework

        
        for l in range(leds.n):
            c = [100, 100, 100]
            
            v = np.linalg.norm(points[:,l]-firework) # if led is in range of firework
            if v < self.r:
                c = self.col
            
            for p in self.particles:
                x,y,z = self.xyz(dt*self.c/30, p)
                v = np.linalg.norm(points[:,l]-[x,y,z])
                if v < 10:
                    c = p['color']
            
            leds.setColor(l, c)
        
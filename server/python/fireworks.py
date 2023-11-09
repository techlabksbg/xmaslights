from program import Program
import time
import math
import random
import numpy as np

class Fireworks(Program):
    def __init__(self, config):
        self.config = config
        self.start = time.time()
        self.r = 10
        self.g = 9.81
        self.c_f = 250
        self.c_p = 10
        self.col = [random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)]
        self.particles = []

    def xyz(self, time, particle): # returns x,y,z coordinates of particle at time
        z = particle['z0'] + particle['v0']*math.sin(particle['theta'])*time - 0.5*self.g*time**2
        y = particle['y0'] + particle['v0']*math.cos(particle['theta'])*math.cos(particle['phi'])*time
        x = particle['x0'] + particle['v0']*math.cos(particle['theta'])*math.sin(particle['phi'])*time
        return x,y,z
    
    def get_particles(self, sphere): # sets self.particles to list of evenly distributed particles around sphere
        num_particles = 30

        phi = random.uniform(0.0, 1.0) * math.pi * (math.sqrt(5.) - 1.)  # golden angle in radians
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

            theta = math.atan2(p[1], p[0])
            phi = math.atan2(math.sqrt(p[0]**2+p[1]**2), p[2])

            self.particles.append({'x0':x, 'y0':y, 'z0':z, 'theta':theta, 'phi':phi, 'v0':20, 'color':self.col, 't0':time.time()})
        

    def step(self, leds, points):

        dt = (time.time()-self.start)/self.config['period']
        z = min(points[2])+dt*self.c_f
        firework = [0, 0, z]

        if (z > max(points[2])-2*self.r):
            self.start = time.time()
            dt = 0
            
            # explode firework
            self.get_particles(firework)
            
            z = min(points[2])
            firework = [0, 0, z]

            self.col = [random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)]

        
        new_particles = [] # get xyz of all particles and remove particles that are out of range
        for p in self.particles:
            dt = (p['t0']-time.time())/self.config['period']
            x,y,z = self.xyz(dt*self.c_p, p)
            p['x'] = x
            p['y'] = y
            p['z'] = z
            if (z > min(points[2]) and y < max(points[1]) and y > min(points[1]) and x < max(points[0]) and x > min(points[0])):
                new_particles.append(p)
        self.particles = new_particles

        for l in range(leds.n):
            col = [50, 50, 50]
            col = [0, 0, 0]
            
            v = np.linalg.norm(points[:,l]-firework) # if led is in range of firework
            if v < self.r:
                col = self.col
            
            for p in self.particles:
                v = np.linalg.norm(points[:,l]-[p['x'], p['y'], p['z']])
                if v < 8:
                    col = p['color']
            
            leds.setColor(l, col)

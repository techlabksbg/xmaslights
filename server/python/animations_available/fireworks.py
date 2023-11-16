from program import Program
import time
import math
import random
import numpy as np

class Fireworks(Program):

    def __init__(self, config):
        self.config = config
        self.start = time.time()

        self.firework = {'rad':10, 'const':250, 'coords':[0, 0, 0]}
        self.particle = {'rad':8, 'const':10}

        self.g = 9.81

        self.col = [random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)]

        self.particles = []

    def xyz(self, time, particle): # returns x,y,z coordinates of particle at time
        # initial velocity in x,y,z directions
        v_0_z = particle['v0']*particle['z0']
        v_0_y = particle['v0']*particle['y0']
        v_0_x = particle['v0']*particle['x0']

        # projectile motion equations
        z = particle['z0']+particle['sphere'][2] + v_0_z*time - 0.5*self.g*time**2
        y = particle['y0']+particle['sphere'][1] + v_0_y*time
        x = particle['x0']+particle['sphere'][0] + v_0_x*time

        return x,y,z
    
    def get_particles(self): # sets self.particles to list of evenly distributed particles around sphere
        # according to https://extremelearning.com.au/how-to-evenly-distribute-points-on-a-sphere-more-effectively-than-the-canonical-fibonacci-lattice/
        num_particles = 30

        n = 50
        golden_ratio = (1 + 5**0.5)/2
        points = np.arange(0, num_particles) # list from 0 to num_particles-1

        theta = 2 * math.pi * points / golden_ratio # longitude
        phi = np.arccos(1 - 2*(points+0.5)/n) # angle from z axis

        # add noise
        add = np.random.normal(0, 0.5)
        theta += add
        phi += add
        
        # [x_i,y_i,z_i] is unit vector
        x, y, z = np.cos(theta) * np.sin(phi), np.sin(theta) * np.sin(phi), np.cos(phi)

        for p in range(num_particles):
            self.particles.append({'x0':x[p], 'y0':y[p], 'z0':z[p], 'rad':self.firework['rad'], 'sphere':self.firework['coords'], 'v0':20, 'color':self.col, 't0':time.time()})
        

    def step(self, leds, points):

        dt = (time.time()-self.start)/self.config['period']
        z = min(points[2])+dt*self.firework['const']
        self.firework['coords'] = [0, 0, z]

        if (z > max(points[2])-2*self.firework['rad']):
            self.start = time.time()
            dt = 0
            
            # explode firework
            self.get_particles()
            
            # new firework from bottom
            z = min(points[2]) 
            self.firework['coords'] = [0, 0, z]

            self.col = [random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)]

        
        # get new coordinates for each particle
        new_particles = []
        for p in self.particles:
            dt = (p['t0']-time.time())/self.config['period']
            p['x'], p['y'], p['z'] = self.xyz(dt*self.particle['const'], p) # get new coordinates
            
            # check if particle is in range
            if (p['z'] > min(points[2]) \
                and p['y'] < max(points[1]) and p['y'] > min(points[1])\
                and p['x'] < max(points[0]) and p['x'] > min(points[0])):
                new_particles.append(p)
        self.particles = new_particles

        # update leds
        for l in range(leds.n):
            col = [20, 20, 20]
            
            v = np.linalg.norm(points[:,l]-self.firework['coords'])
            if v < self.firework['rad']: # if led is in range of firework
                col = self.col
            
            for p in self.particles:
                v = np.linalg.norm(points[:,l]-[p['x'], p['y'], p['z']])
                if v < self.particle['rad']: # if led is in range of particle
                    col = p['color']
            
            leds.setColor(l, col)

    def defaults(self):
        return {'params':{'brightness':0.1, 
                          'saturation':1.0, 
                          'period':10,
                          'dir':'0,0,1',
                          'scale':100},
                'autoplay':20}

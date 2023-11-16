from program import Program
import time
import math
import colorsys
import colorsys
import random
import numpy as np

# Ideen zur Performance-Steigerung:
#  - Weniger Partikel mit grösseren Radien
#  - Alles mit Vektor- oder Matrix-Operationen lösen
# 
# Anstatt Partikel:
# Eine einzige Kugel(schicht) mit Noise-Funktion auf die
# Kugel projiziert, siehe z.B.
# https://en.wikipedia.org/wiki/Perlin_noise


class Fireworks(Program):

    def __init__(self, config):
        self.config = config
        self.start = time.time()

        self.firework = {'rad':12, 'const':500, 'coords':[0, 0, 0]}
        self.particle = {'rad':6, 'const':10, 'vel':20}
        self.num_particles = 500

        self.wait = 5 # how many seconds to wait from explosion to next firework

        self.pad = 30 # how far from top to explode firework

        self.g = 9.81

        self.hue = random.random()

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

        golden_ratio = (1 + 5**0.5)/2
        points = np.arange(0, self.num_particles) # list from 0 to num_particles-1

        theta = 2 * math.pi * points / golden_ratio # longitude
        phi = np.arccos(1 - 2*(points+0.5)/self.num_particles) # angle from z axis

        # add noise
        add = np.random.normal(0, 0.5)
        theta += add
        phi += add
        
        # [x_i,y_i,z_i] is unit vector
        x, y, z = np.cos(theta) * np.sin(phi), np.sin(theta) * np.sin(phi), np.cos(phi)

        for p in range(self.num_particles):
            self.particles.append({'x0':x[p], 'y0':y[p], 'z0':z[p], 'rad':self.firework['rad'], 'sphere':self.firework['coords'], 'v0':self.particle['vel'], 'hue':self.hue, 't0':time.time()})
        

    def step(self, leds, points):

        dt = (time.time()-self.start)/self.config['period']
        z = min(points[2])+dt*self.firework['const']
        self.firework['coords'] = np.array([0, 0, z])

        if (z > max(points[2])-2*self.firework['rad']-self.pad):
            # explode firework
            self.get_particles()
            
            self.start = time.time()+self.wait # wait some time before next firework
            dt = (time.time()-self.start)/self.config['period']
            
            # new firework from bottom
            z = min(points[2])+dt*self.firework['const']
            self.firework['coords'] = np.array([0, 0, z])

            self.hue = random.random()

        
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
        len_firework = np.linalg.norm(points-self.firework['coords'].reshape(3,1), axis=0) # get dist to firework
        len_particles = np.array([math.inf] * len(points[0]))
        hue_particle = [0] * len(points[0])

        for p in self.particles:
            p_coords = np.array([p['x'], p['y'], p['z']])

            new_len_particles = np.linalg.norm(points-p_coords.reshape(3,1), axis=0) # get the dist to particle p
            replaced = (new_len_particles<=len_particles) # if we need to update the color

            len_particles = np.minimum(len_particles, new_len_particles) # the led chooses the nearest particle
            hue_particle = ~replaced*hue_particle + replaced*p['hue'] # update color accordingly

        for l in range(leds.n):
            col = [0, 0, 0]
            
            if (len_firework[l] < self.firework['rad']):
                col : list(int,int,int) = [int(x*255) for x in colorsys.hsv_to_rgb(self.hue, self.config['saturation'], self.config['brightness'])]
            if (len_particles[l] < self.particle['rad']):
                col : list(int,int,int) = [int(x*255) for x in colorsys.hsv_to_rgb(hue_particle[l], self.config['saturation'], self.config['brightness'])]
            
            leds.setColor(l, col)

    def defaults(self):
        return {'params':{'brightness':0.1, 
                          'saturation':1.0, 
                          'period':10},
                'autoPlay': True,
                'playFor':30,
                'web':True}

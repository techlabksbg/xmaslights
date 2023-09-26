import pygame
import numpy as np
import math
from python.leds import LEDs
from python.rainbow3d import Rainbow3d


def init():
    with open("python/3ddata.txt", "r") as f:
        points = np.column_stack([[float(c) for c in l.split(" ")][0:3] for l in f.readlines()])
    return points

def rotationz(w):
    c = math.cos(w)
    s = math.sin(w)
    return np.column_stack([[c,s,0],[-s,c,0],[0,0,1]])

def transform(points):
    minz = min(points[2])
    maxz = max(points[2])
    scale = 640/(maxz-minz)
    return np.column_stack([[-scale,0,0,0],[0,scale,0,0],[0,0,-scale,0],[500, 0, 320, 1]])


    

def run(points, leds, prog):
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    t = transform(points)
    running = True
    w = 0.0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill("black")
        rotated = np.matmul(rotationz(w), points)
        rotated = np.append(rotated, [np.ones(leds.n)], axis=0)

        transformed = np.matmul(t, rotated)
        
        prog.step(leds, points)
        for l in range(leds.n):
            c = pygame.Color(int(leds.leds[l][0]), int(leds.leds[l][1]), int(leds.leds[l][2]))
            s = 500/transformed[0][l]
            pygame.draw.circle(screen,
                                c,
                               (transformed[1][l]*s+640, transformed[2][l]*s+360),
                               4)

        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000
        w+=0.01
    pygame.quit()



points = init()
numleds = len(points[0])
leds = LEDs(numleds)  # RGB is assumed
prog = Rainbow3d()

run(points, leds, prog)

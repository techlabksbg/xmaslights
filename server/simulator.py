import pygame
import numpy as np
import math

# Installation von pygame unter Windows (auf der Kommandozeile):
# pip install pygame

# Unter Ubuntu-Linux (und wohl andere Debian-basierte Distros)
# sudo apt install python3-pygame

# Eigene Dinge importieren
from python.leds import LEDs
from python.rainbow3d import Rainbow3d

aufloesung = (1280, 720)

# Punkte einlesen
def init():
    # Koordinaten der LEDs einlesen
    # Als np.array, geeignet für Matrix-Operationen, 
    # x-Koordinate von Punkt 5 ist poins[0][5] (Erst Zeile, dann Spalte)
    with open("python/3ddata.txt", "r") as f:
        points = np.column_stack([[float(c) for c in l.split(" ")][0:3] for l in f.readlines()])
    return points

# 3D-Rotationsmatrix um z
def rotationz(w):
    c = math.cos(w)
    s = math.sin(w)
    return np.column_stack([[c,s,0],[-s,c,0],[0,0,1]])

def getHeight(points):
    minz = min(points[2])
    maxz = max(points[2])
    return maxz-minz

# TODO
# Zentralprojektion auf die y,z-Ebene
def projektion(x,y,z, scale, aufloesung):

    a = y+aufloesung[0]/2
    b = -z + aufloesung[1]
    r = 4  # Optional: Radius je nach Distanz für besseren 3D-Effekt.

    return a,b,r

def run(points, leds, prog):
    pygame.init()
    screen = pygame.display.set_mode(aufloesung)
    clock = pygame.time.Clock()
    height = getHeight(points)
    running = True
    w = 0.0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill("black")

        # Punkte rotieren
        rotated = np.matmul(rotationz(w), points)

        # Farben berechnen 
        prog.step(leds, points)

        # Alle Leds zeichnen
        for l in range(leds.n):
            # Farbe für LED l auslesen und konvertieren
            c = pygame.Color(int(leds.leds[l][0]), int(leds.leds[l][1]), int(leds.leds[l][2]))

            x,y,r = projektion(rotated[0][l], rotated[1][l], rotated[2][l], height, aufloesung)

            # Kreis zeichnen
            pygame.draw.circle(screen, c, (x, y), r)

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

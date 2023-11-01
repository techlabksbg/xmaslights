import pygame
import numpy as np
import math
import socket
import time

# Installation von pygame unter Windows (auf der Kommandozeile):
# pip install pygame

# Unter Ubuntu-Linux (und wohl andere Debian-basierte Distros)
# sudo apt install python3-pygame

SERVER_IP = "127.0.0.1"
SERVER_PORT = 15878
RESOLUTION = (1280,720)
RGBORDER = (1,0,2)

def projektion(x,y,z, height, aufloesung):
    kx, ky, kz = 150, 0, 100
    a = ky+kx/(kx-x)*(y-ky)
    b = kz+kx/(kx-x)*(z-kz)
    scale = aufloesung[1]/height
    a *= scale
    b *= scale 
    a += aufloesung[0]/2
    b = aufloesung[1]-b
    r = 8*(kx/(kx-x))**2  # Optional: Radius je nach Distanz für besseren 3D-Effekt.

    return a,b,r

# 3D-Rotationsmatrix um z
def rotationz(w):
    c = math.cos(w)
    s = math.sin(w)
    return np.column_stack([[c,s,0],[-s,c,0],[0,0,1]])

class Simulator:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(0)

        with open("3ddata.txt", "r") as f:
            self.points = np.column_stack([[float(c) for c in l.split(" ")][0:3] for l in f.readlines()])
        self.height = max(self.points[2]) - min(self.points[2])
        self.n = self.points.shape[1]
        self.colors = [[0,0,0] for i in range(n)]




    def run(self):
        pygame.init()
        screen = pygame.display.set_mode(RESOLUTION)
        clock = pygame.time.Clock()
        w = 0
        lastData = 0
        lastPing = 0
        while running:
            if (time.time()-lastPing>1):
                if (lastData==0 or (lastData>0 and time.time()-lastData>5)):
                    self.socket.send(b"start")
                    lastPing = time.time()
                else:
                    lastPing = time.time()
                    self.socket.send(b"ping")




            for event in pygame.event.get():
                # Quit on keypressed
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    running = False
                # Quit on window close
                if event.type == pygame.QUIT:
                    running = False
            screen.fill("black")

            # Punkte rotieren
            rotated = np.matmul(rotationz(w), points)

            # Alle Leds zeichnen
            for l in range(leds.n):
                # Farbe für LED l auslesen und konvertieren
                c = pygame.Color(self.colors[l][RGBORDER[0]], self.colors[l][RGBORDER[1]], self.colors[2][RGBORDER[2]])

                x,y,r = projektion(rotated[0][l], rotated[1][l], rotated[2][l], self.height, RESOLUTION)

                # Kreis zeichnen
                pygame.draw.circle(screen, c, (x, y), r)

            pygame.display.flip()

            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            dt = clock.tick(60) / 1000
            w+=0.01
        pygame.quit()


def run(points, leds, prog):
    while running:
        for event in pygame.event.get():
            # Quit on keypressed
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                running = False
            # Quit on window close
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

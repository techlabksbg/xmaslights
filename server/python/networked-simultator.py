import pygame
import numpy as np
import math
import socket
import time
import threading

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
    r = 2*(kx/(kx-x))**2  # Optional: Radius je nach Distanz für besseren 3D-Effekt.

    return a,b,r

# 3D-Rotationsmatrix um z
def rotationz(w):
    c = math.cos(w)
    s = math.sin(w)
    return np.column_stack([[c,s,0],[-s,c,0],[0,0,1]])

class DataGrabber():
    def __init__(self, socket, colors):
        self.socket = socket
        self.nextPacket = 0
        self.bufindex = 0
        self.colors = colors
        self.framesok = 0
        self.framesbad = 0
        self.lastData = 0
        self.connectionBroken = False

    def run(self):
        def loop():
            while True:
                time.sleep(0.0005)
                if self.connectionBroken:
                    continue
                try:
                    message, _ = self.socket.recvfrom(1024)
                    l = len(message)
                    if l>0:                        
                        self.lastData = time.time()
                    #print(f"m[0]={message[0]}")
                    # print(f"len={l}, m0={message[0]}")
                    if message[0]==254 and message[1:]==b"pong":
                        print("got pong")
                        continue
                    if (l>1 and (message[0]==self.nextPacket or message[0]==255)):
                        if (self.nextPacket==0):
                            self.bufindex = 0
                        # Copy data
                        for i in range(1,l):
                            c = self.bufindex+i-1
                            if (c//3>=len(self.colors)):
                                self.bufindex = 0
                                c = 0
                            self.colors[c//3][c%3] = message[i]
                        self.bufindex+=l-1
                        if message[0]==255: # Last packet
                            #print(f"eom, bufindex={self.bufindex}")
                            if self.bufindex==len(self.colors)*3:
                                self.framesok+=1
                            else:
                                self.framesbad+=1
                            if (self.framesbad+self.framesok)%100==0:
                                print(f"ok={self.framesok}, bad={self.framesbad}")
                            self.bufindex = 0
                            self.nextPacket = 0
                        else:
                            self.nextPacket+=1
                        continue
                    # Wrong packet number
                    self.nextPacket = 0
                    self.bufindex = 0
                    self.framesbad+=1
                    if (self.framesbad+self.framesok)%100==0:
                        print(f"ok={self.framesok}, bad={self.framesbad}")
                except socket.timeout: 
                    pass
                except BlockingIOError:
                    pass
                except ConnectionResetError:
                    self.connectionBroken = True
                    print("Windows Error 10054, waiting to reconnect...")
                except OSError:
                    self.connectionBroken = True
                    print("Windows Error 10022... what ever...")
            
        t = threading.Thread(target=loop)
        t.daemon = True  # Shutdown if main thread terminates
        t.start()

class Simulator:
    def __init__(self):
        self.socket = False
        self.openSocket()

        with open("3ddata.txt", "r") as f:
            self.points = np.column_stack([[float(c) for c in l.split(" ")][0:3] for l in f.readlines()])
        self.height = max(self.points[2]) - min(self.points[2])
        self.n = self.points.shape[1]
        self.colors = [[0,0,0] for i in range(self.n)]

    def openSocket(self):
        if self.socket:
            self.socket.close()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self.socket.settimeout(0)


    def run(self):
        pygame.init()
        screen = pygame.display.set_mode(RESOLUTION)
        clock = pygame.time.Clock()
        dw = 0.01
        w = 0
        lastPing = 0
        dataGrabber = DataGrabber(self.socket, self.colors)
        dataGrabber.run()
        running = True
        startCounter = 3
        while running:
            if (dataGrabber.connectionBroken):
                print("Reopening socket...")
                self.openSocket()
                dataGrabber.socket = self.socket
                dataGrabber.connectionBroken = False
                startCounter=3
            if (time.time()-lastPing>1):
                if (dataGrabber.lastData==0 or (dataGrabber.lastData>0 and time.time()-dataGrabber.lastData>5)):
                    self.socket.sendto(b"start", (SERVER_IP, SERVER_PORT))
                    print("Sent start")
                    lastPing = time.time()
                    startCounter-=1
                    if (startCounter<=0):
                        print("Reopening socket...")
                        self.openSocket()
                        dataGrabber.socket = self.socket
                        dataGrabber.connectionBroken = False
                        startCounter=3
                else:
                    lastPing = time.time()
                    self.socket.sendto(b"ping", (SERVER_IP, SERVER_PORT))
                    print("Sent ping")

            for event in pygame.event.get():
                # Quit on keypressed
                if event.type == pygame.KEYDOWN:   #or event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        running = False
                    if event.key == pygame.K_x:
                        w = 0
                        dw = 0
                    if event.key == pygame.K_y:
                        w = math.pi/2
                        dw = 0
                    if event.key == pygame.K_a:
                        dw -= 0.005
                    if event.key == pygame.K_d:
                        dw += 0.005
                    if event.key == pygame.K_s:
                        dw = 0

                # Quit on window close
                if event.type == pygame.QUIT:
                    running = False
            screen.fill("black")

            # Punkte rotieren
            rotated = np.matmul(rotationz(w), self.points)

            def gamma(x):
                return int((x/255)**0.5*255)

            # Alle Leds zeichnen
            for l in range(self.n):
                # Farbe für LED l auslesen und konvertieren
                c = pygame.Color(gamma(self.colors[l][RGBORDER[0]]), gamma(self.colors[l][RGBORDER[1]]), gamma(self.colors[l][RGBORDER[2]]))

                x,y,r = projektion(rotated[0][l], rotated[1][l], rotated[2][l], self.height, RESOLUTION)

                # Kreis zeichnen
                pygame.draw.circle(screen, c, (x, y), r)

            pygame.display.flip()

            dt = clock.tick(60) / 1000
            w+=dw
        pygame.quit()


Simulator().run()

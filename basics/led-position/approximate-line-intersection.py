import numpy as np
import sys

def init():
    if len(sys.argv)<3:
        print("Bitte zwei Dateinamen angeben")
    data = []
    for datei in sys.argv[1:]:
        with open(datei,"r") as f:
            cam = f.readline().split(' ')
            cam = [float(c) for c in cam]
            leds = f.readlines()
            leds = [[float(c) for c in x.split(' ')] for x in leds]            
            data.append([cam, leds])
    return data

def approxInter(cams, points):
    cams = [np.array(k) for k in cams]
    points = [np.array(p) for p in points]
    r = [points[i]-cams[i] for i in range(2)]
    # Vektor in Richtung der kürzesten Verbindung
    n = np.cross(r[0], r[1])
    # Normalvektoren zu den Ebenen E1 und E2
    ni = [np.cross(n, ri) for ri in r]
    # Parameter d der Ebenen E1 und E2
    di = [-np.dot(cams[i], ni[i]) for i in range(2)]
    # Paremters t
    ti = [(-di[i]-np.dot(ni[i],cams[1-i]))/  \
          np.dot(ni[i],r[1-i]) for i in range(2)]
    p = [ti[i]*r[i]+cams[i] for i in range(2)]

    return (p[0]+p[1])/2    

data = init()

cams = [data[0][0], data[1][0]]
print(cams)
for i in range(len(data[0][1])):
    leds = [data[0][1][i][0:3], data[1][1][i][0:3]]
    p = approxInter(cams, leds)
    print(leds)
    print(p)
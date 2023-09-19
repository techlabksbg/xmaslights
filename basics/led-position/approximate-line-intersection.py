import numpy as np
import sys

def init():
    if len(sys.argv)<3:
        print("Bitte mindestens zwei Dateinamen angeben")
    data = []
    for datei in sys.argv[1:]:
        with open(datei,"r") as f:
            cam = f.readline().split(' ')
            cam = [float(c) for c in cam]
            leds = f.readlines()
            leds = [[float(c) for c in x.split(' ')] for x in leds]            
            data.append([cam, leds])
    return data

def approxInter(cams, points, confidence=[1,1]):
    # in numpy Vektoren umwandeln
    cams = [np.array(k) for k in cams]
    points = [np.array(p) for p in points]
    # Richtungsvektoren
    ri = [points[i]-cams[i] for i in range(2)]
    # Vektor in Richtung der kürzesten Verbindung
    n = np.cross(ri[0], ri[1])
    # Normalvektoren der Ebenen E1 und E2
    ni = [np.cross(n, r) for r in ri]
    # Parameter d der Ebenen E1 und E2
    di = [-np.dot(cams[i], ni[i]) for i in range(2)]
    # Parameter t für die Punkte auf der Gerade der kürzesten Verbindung
    ti = [(-di[i]-np.dot(ni[i],cams[1-i]))/  \
          np.dot(ni[i],ri[1-i]) for i in range(2)]
    # Punkte auf der Geraden der kürzestens Verbindung
    pi = [ti[i]*ri[i]+cams[i] for i in range(2)]
    distance = np.linalg.norm(pi[1]-pi[0])
    # Gewichteter Mittelpunkt der Punkte
    m = (pi[0]*confidence[0]+pi[1]*confidence[1])/(np.sum(confidence))
    c = (confidence[0]+confidence[1])/2*(10/(5+distance))
    if (c>1):
        c=1.0
    return (m,c)

data = init()
numfiles = len(data)
numleds = len(data[0][1])

points = [[] for i in range(numleds)]

for i in range(numfiles-1):
    for j in range(i+1,numfiles):
        cams = [data[i][0], data[j][0]]
        #print(cams)
        for l in range(numleds):
            leds = [data[i][1][l][0:3], data[j][1][l][0:3]]
            confidence = [data[0][1][l][3], data[j][1][l][3]]
            p = approxInter(cams, leds,confidence)
            points[l].append(p)

#print(points)
final = [max(p, key=lambda x:x[1]) for p in points]
#print(final)
for f in final:
    print("%f %f %f %f" % (f[0][0], f[0][1], f[0][2],f[1]))

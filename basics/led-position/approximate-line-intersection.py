import numpy as np
import sys

def init():
    if len(sys.argv)<3:
        print("Bitte mindestens zwei Dateinamen angeben")
        quit()
    data = [] 
    for datei in sys.argv[1:]:
        with open(datei,"r") as f:
            cam = f.readline().split(' ')
            cam = [float(c) for c in cam]
            leds = f.readlines()
            leds = [[float(c) for c in x.split(' ')] for x in leds]
            leds = [{'point':led[0:3], 'confidence':led[3]} for led in leds] # Dictionary for better code
            data.append({'cam': cam, 'leds':leds})   # Dictionary for better code
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
    return {'point':m, 'confidence':c}

data = init()
numfiles = len(data)
numleds = len(data[0]['leds'])

results = [[] for i in range(numleds)]

for i in range(numfiles-1):
    for j in range(i+1,numfiles):
        cams = [data[i]['cam'], data[j]['cam']]
        #print(cams)
        for l in range(numleds):
            leds = [data[i]['leds'][l]['point'], data[j]['leds'][l]['point']]
            confidence = [data[i]['leds'][l]['confidence'], data[j]['leds'][l]['confidence']]
            p = approxInter(cams, leds, confidence)
            results[l].append(p)

# Extract the point with highest confidence
# Alternatively one could weigth the points by confidence
final = [max(res, key=lambda r:r['confidence']) for res in results]

for f in final:
    point = f['point']
    confidence = f['confidence']
    print("%.1f %.1f %.1f %.2f" % (point[0], point[1], point[2],confidence))

import cv2
import os
import sys
import re
import numpy as np

n=0 #define immage counter

# Produces an array with all files
def init():
    if len(sys.argv)<2:
        print("Bitte das Verzeichnis mit den Bildern angeben.")
        print("z.B. python analyze_images.py temp/20230909_192342 > ausgabe_datei.txt")
        exit()
    dir = sys.argv[1]
    if not os.path.isdir(dir):
        print(f"Das Verzeichnis {dir} existiert nicht.")
        exit()
    if os.path.isfile(dir+"/campos.txt"):
        with open(dir+"/campos.txt") as f:
            print(f.read(), end="")
    else:
        print("? ? ?\n?");
    return sorted([dir+"/"+f for f in os.listdir(dir) if re.match(r"\d{4}\.png$",f)])

def find_brightest_pixel(image):
    # Find the coordinates of the brightest pixel
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(image)
    brightest_pixel = maxLoc
    brightness = maxVal

    return brightest_pixel, brightness


def simple(image,data):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return find_brightest_pixel(gray), 0.3  # No further investigation (so we should catch about 30% of the LEDs correctly)

def blurred(image,data):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (13,13), 0)
    return find_brightest_pixel(blurred), 0.4 # Like simple, but might capture the center more precisely

def threshold_blurred(image,data):
    maxbrightness = data[0][3]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray,maxbrightness-10,255,cv2.THRESH_TOZERO)
    blurred = cv2.GaussianBlur(thresh, (13,13), 0)
    return find_brightest_pixel(blurred), 0.5 # Should capture about half of the LEDs quite reliably

files = init()
numleds = len(files)
data = []  # n entries of the form [(((x,y),br),prob), ...]
images = []
imagesum = None

# First pass:
for n,f in enumerate(files):
    data.append([])
    image = cv2.imread(f)
    images.append(image)
    if (type(imagesum)==type(None)):
        imagesum = np.zeros(image.shape, dtype=np.uint32)
    imagesum += image
    for method in [simple, threshold_blurred]:
        d = method(image, data[n])
        d = (d[0][0][0], d[0][0][1], d[0][1], d[1])
        data[n].append(d)


imagesum //= len(files)
imagesum = np.uint8(imagesum)




numleds = len(data)
top_n = min(range(numleds), key=lambda i:data[i][1][1])
bottom_n = 0 # max(range(numleds), key=lambda i:data[i][2][0][0][1])

#print("top_n=%d, bottom_n=%d (should be 0)" % (top_n, bottom_n))
#print(data[top_n])
#print(data[bottom_n])

top = data[top_n][1][0:3]
bottom = data[bottom_n][1][0:3]

e2 = np.array([top[0]-bottom[0],top[1]-bottom[1]])
e1 = np.array([-e2[1], e2[0]])
o = np.array([bottom[0], bottom[1]])

a = np.matrix([e1, e2, o]).transpose()
#print(a);

polygon = np.matrix([[0,-0.05,1],[0.4,0.05,1],[0.05, 1.05,1], [-0.05, 1.05 ,1], [-0.4,0.05,1]]).transpose()

points = a*polygon;
#print(points);

mask = np.zeros(image.shape, dtype=np.uint8)
cv2.fillPoly(mask, pts=np.int32([points.transpose()]),color=(255,255,255))


# Second pass:
data1st = data
data = []
for n,img in enumerate(images):
    data.append([])
    image = images[n]#-cv2.min(images[n],imagesum)
    image = cv2.bitwise_and(image, mask)
    for method in [simple, threshold_blurred]:
        d = method(image, data[n])
        d = (d[0][0][0], d[0][0][1], d[0][1], d[1])
        data[n].append(d)
    for i,p in enumerate(data[n]):
        color = ((0,0,255), (0,255,0), (255,0,0))[i]
        cv2.circle(image, (p[0], p[1]), 8+4*i, color,  2)
    #cv2.imshow("image", image)
    #cv2.waitKey(50)

data2 = data
data = []
distances=[]
for n in range(len(images)):
    p1 = np.array(data2[n][0][0:2])
    p2 = np.array(data2[n][1][0:2])
    if np.linalg.norm(p1-p2)<5:
        p = p2
        confidence = 0.7
    else:
        confidence = 0.7*5/np.linalg.norm(p1-p2)
        p = p1
    data.append([p, confidence])
    if (n>0):
        distances.append(np.linalg.norm(data[n-1][0]-p))
data[0][1]=1.0
data[top_n][1]=1.0
distances = np.array(distances)
meandist = np.median(distances)
stddev = np.std(distances)
for i in range(1,numleds-1):
    if distances[i-1]<meandist+stddev/2 and distances[i]<meandist+stddev/2:
        data[i][1] += (1-data[i][1])/2
    if distances[i-1]>meandist+stddev and distances[i]>meandist+stddev:
        data[i][1]/=2
    
#print(data)
print("%d %d" % (bottom_n, top_n))    
for i in range(numleds):
    print("%d %d %d %f" % (i, data[i][0][0], data[i][0][1], data[i][1]))

import cv2
import os
import sys
import re
import numpy as np

n=0 #define immage counter
mask = None
noleds = None

# Produces an array with all files
def init():
    global mask, noleds
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
        print("? ? ?\n? ?")
    
    maskpath = dir+"/mask.png"
    if os.path.exists(maskpath):
        mask = cv2.imread(maskpath)
    
    nonepath = dir+"/none.png"
    if os.path.exists(nonepath):
        noleds = cv2.imread(nonepath)
        
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

def difference(image, data):
    diff = image.astype("float") - noleds.astype("float")
    diff[diff<0]=0
    diff = diff.astype("uint8")
    #cv2.imshow("image", diff)
    #cv2.waitKey(500)
    return threshold_blurred(diff, data)

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

if mask is None:
    polygon = np.matrix([[180,480],[180,0],[460,0], [460, 480]]).transpose()
    mask = np.zeros([480,640,3], dtype=np.uint8)
    cv2.fillPoly(mask, pts=np.int32([polygon.transpose()]),color=(255,255,255))

data = []
for n,f in enumerate(files):
    data.append([])
    image = cv2.imread(f)
    image = cv2.bitwise_and(image, mask)
    for method in [simple, threshold_blurred, difference]:
        d = method(image, data[n])
        d = (d[0][0][0], d[0][0][1], d[0][1], d[1])
        data[n].append(d)
#    for i,p in enumerate(data[n]):
#        color = ((0,0,255), (0,255,0), (255,0,0))[i]
#        cv2.circle(image, (p[0], p[1]), 8+4*i, color,  2)
#    cv2.imshow("image", image)
#    cv2.waitKey(500)

bottom_n = 0 # max(range(numleds), key=lambda i:data[i][2][0][0][1])
top_n = min([i for i in range(numleds) if abs(data[i][2][0]-data[bottom_n][2][0])<20], key=lambda i:data[i][1][1])

data2 = data
data = []
distances=[]

mousex = 0
mousey = 0
clicked = False
def mouseCallBack(event,x,y,flags, param):
    global mousex, mousey,clicked
    clicked = event == cv2.EVENT_LBUTTONDOWN
    if clicked:
        mousex = x
        mousey = y
    

cv2.namedWindow("image")
cv2.setMouseCallback('image', mouseCallBack)
def getUserCoords(nr):
    #print(f"Ask user where led {nr} is...")
    images = [cv2.imread(files[(x+numleds)%numleds]) for x in range(nr-1, nr+2)]

    cv2.imshow("image", images[1])
    cv2.waitKey(10)
    while clicked:
        cv2.waitKey(10)
    c = 0
    while not clicked:
        c = c+1
        if c%20==0:
            cv2.imshow("image", images[0])
        if c%20==1:
            cv2.imshow("image", images[2])
        if c%20==2:
            cv2.imshow("image", images[1])

        cv2.waitKey(50)
    #print(f"User says {mousex} {mousey}")
    return mousex, mousey


    

for n in range(numleds):
    p0 = np.array(data2[n][0][0:2])
    p1 = np.array(data2[n][1][0:2])
    p2 = np.array(data2[n][2][0:2])
    if (np.linalg.norm(p0-p1)+np.linalg.norm(p0-p2)+np.linalg.norm(p1-p2))<15:
        #print(f"all agree on {n}")
        p = p2
        confidence = 0.9
    elif np.linalg.norm(p0-p2)<8:
        #print(f"0 and 2 agree on {n}")
        p = p2
        confidence = 0.7
    elif np.linalg.norm(p1-p2)<8:
        p = p2
    else: # ask the user
        #print(f"Norms 01: {np.linalg.norm(p0-p1)}, 02: {np.linalg.norm(p0-p2)}, 12: {np.linalg.norm(p2-p1)}")
        x,y = getUserCoords(n)
        p = np.array([x,y])
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
    if (i%200!=0):
        if distances[i-1]<meandist+stddev/2 and distances[i]<meandist+stddev/2:
            data[i][1] += (1-data[i][1])/2
        if distances[i-1]>meandist+stddev and distances[i]>meandist+stddev:
            data[i][1]/=2
    
#print(data)
print("%d %d" % (bottom_n, top_n))    
for i in range(numleds):
    print("%d %d %d %f" % (i, data[i][0][0], data[i][0][1], data[i][1]))

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
    maxbrightness = data[0][1]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray,maxbrightness-10,255,cv2.THRESH_TOZERO)
    blurred = cv2.GaussianBlur(thresh, (13,13), 0)
    return find_brightest_pixel(blurred), 0.5 # Should capture about half of the LEDs quite reliably

files = init()
data = []  # n entries of the form [(((x,y),br),prob), ...]

# First pass:
for n,f in enumerate(files):
    data.append([])
    image = cv2.imread(f)
    for method in [simple, blurred, threshold_blurred]:
        data[n].append(method(image,data[n]))

numleds = len(data)
top_n = min(range(numleds), key=lambda i:data[i][2][0][0][1])
bottom_n = max(range(numleds), key=lambda i:data[i][2][0][0][1])

print("top_n=%d, bottom_n=%d (should be 0)" % (top_n, bottom_n))
print(data[top_n])
print(data[bottom_n])

top = data[top_n][2][0][0]
bottom = data[bottom_n][2][0][0]

e2 = np.array([top[0]-bottom[0],top[1]-bottom[1]])
e1 = np.array([e2[1], -e2[0]])
o = np.array([bottom[0], bottom[1]])

a = np.matrix([e1, e2, o]).transpose()
print(a);

polygon = np.matrix([[0,0,1],[0.4,0.05,1],[0.05, 1.0,1], [-0.05, 1.0,1], [-0.4,0.05,1]]).transpose()

points = a*polygon;
print(points);

mask = np.zeros(image.shape, dtype=np.uint8)
cv2.fillPoly(mask, pts=np.int32([points.transpose()]),color=(255,255,255))

cv2.imshow("mask", mask)
cv2.waitKey(0)

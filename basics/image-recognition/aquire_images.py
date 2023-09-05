import cv2
import requests
from time import sleep 
import os
import sys
from datetime import datetime
import sys

NUMLEDS=50
if len(sys.argv)>1:
    NUMLEDS = int(sys.argv[1])

print(f"scanning {NUMLEDS} LEDs...")


def init():
    global cam, subdir
    cam = cv2.VideoCapture(0)
    temp = "temp"

    if not os.path.isdir(temp):
        print(f"Creating directory {temp}")
        os.mkdir("temp")

    subdir=temp+"/"+datetime.now().strftime("%Y%m%d_%H%M%S")

    print(f"Saving images into directory {subdir}")
    os.mkdir(subdir)


def getImage(led):
    url = f"http://192.168.4.1/cmd?led={led}"
    print(url)
    r = requests.get(url, timeout=3)
    sleep(0.1)
    
    ret, frame = cam.read()
    filename = "%s/%04d.png" % (subdir, led)
    print(f"Saved image to {filename}")
    cv2.imwrite(filename, frame)
    #sleep(0.05)


init();
for led in range(NUMLEDS):
    getImage(led);
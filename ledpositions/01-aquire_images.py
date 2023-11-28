import cv2
import requests
import os
import sys
from datetime import datetime
import sys

NUMLEDS=800
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
    turnOn(NUMLEDS)
    state = 0
    while state<100:
        ret, frame = cam.read()
        cv2.imshow("Image", frame)
        k=cv2.waitKey(50)
        if (k>0):
            state+=1
            if state==1:
                turnOn(-1)
        if (state>0):
            state+=1

def turnOn(led):
    url = f"https://ofi.tech-lab.ch/xmaslights?prg=SingleLED&led={led}&color=ffffff"
    print(url)
    r = requests.get(url, timeout=3)

def getImage(led):
    turnOn(led)
    cv2.waitKey(200)  # Wait for the camera to settle

    ret, frame = cam.read()
    cv2.imshow("Image", frame);
    filename = "%s/%04d.png" % (subdir, led)
    if led==-1:
        filename = f"{subdir}/none.png"
    elif led==NUMLEDS:
        filename = f"{subdir}/all.png"
    print(f"Saved image to {filename}")
    cv2.imwrite(filename, frame)


init()
for led in range(NUMLEDS):
    getImage(led)
getImage(-1)
turnOn(NUMLEDS)
# Let camera settle for full brightness
cv2.waitKey(1000)
getImage(NUMLEDS)
turnOn(-1)
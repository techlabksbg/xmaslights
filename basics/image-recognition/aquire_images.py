import cv2
import requests
import os
import sys
from datetime import datetime
import sys

NUMLEDS=200
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

    for i in range(60):
        ret, frame = cam.read()
        cv2.imshow("Image", frame)
        cv2.waitKey(10)  # Needed for the Display Window

def getImage(led):
    url = f"https://ofi.tech-lab.ch/xmaslights?activeProgram=SingleLED&led={led}&color=ffffff"
    print(url)
    r = requests.get(url, timeout=3)
    cv2.waitKey(200)  # Wait for the camera to settle

    ret, frame = cam.read()
    cv2.imshow("Image", frame);
    filename = "%s/%04d.png" % (subdir, led)
    print(f"Saved image to {filename}")
    cv2.imwrite(filename, frame)


init();
for led in range(NUMLEDS):
    getImage(led);

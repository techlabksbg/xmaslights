import cv2
import os
import sys
import re
import numpy as np

n=0 #define immage counter
mask = None

# Produces an array with all files
def init():
    global mask
    if len(sys.argv)<2:
        print("Bitte das Verzeichnis mit den Bildern angeben.")
        print("z.B. python analyze_images.py temp/20230909_192342 > ausgabe_datei.txt")
        exit()
    dir = sys.argv[1]
    if not os.path.isdir(dir):
        print(f"Das Verzeichnis {dir} existiert nicht.")
        exit()
    maskpath = dir+"/mask.png"
    if os.path.exists(maskpath):
        mask = cv2.imread(maskpath)
    else:
        print(f"Die Maskendatei #{maskpath} existiert nicht.")
        exit()
    return sorted([dir+"/"+f for f in os.listdir(dir) if re.match(r"\d{4}\.png$",f)])

files = init()

for f in files:
    image = cv2.imread(f)
    image = cv2.bitwise_and(image, mask)
    cv2.imwrite(f, image)
    print(f"Masked {f}")

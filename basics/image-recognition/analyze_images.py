import cv2
import os
import sys
import re


n=0 #define immage counter

# Produces an array with all files
def init():
    if len(sys.argv)<2:
        print("Bitte das Verzeichnis mit den Bildern angeben.")
        print("z.B. python analyze_images.py temp/20230909_192342")
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
    # Convert the image to grayscale for simplicity
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Find the coordinates of the brightest pixel
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(grayscale_image)
    brightest_pixel = maxLoc
    brightness = maxVal

    return brightest_pixel, brightness

files = init()
for n,f in enumerate(files):
    image = cv2.imread(f)
    brightest_pixel_coords, brightness_value = find_brightest_pixel(image)
    x,y = brightest_pixel_coords
    print("%04d %d %d 0.5" % (n, x, y))

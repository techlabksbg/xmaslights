import cv2
import os
import sys

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
    return sorted([dir+"/"+f for f in os.listdir(dir)])


files = init()
for f in files:
    print(f"Loading {f}...")
    image = cv2.imread(f)
    cv2.imshow("Image", image)
    cv2.waitKey(500)  # Waits for 500ms and thus allows the image to be displayed

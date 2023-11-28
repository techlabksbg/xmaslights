import cv2
import os
import sys
import numpy as np

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


# Bild laden
bild = cv2.imread('files')

# Bild in Graustufen konvertieren
graustufen_bild = cv2.cvtColor(bild, cv2.COLOR_BGR2GRAY)

# Hellste Stelle im Bild finden
min_wert, max_wert, min_loc, max_loc = cv2.minMaxLoc(graustufen_bild)

# Koordinaten der hellsten Stelle extrahieren
helleste_stelle_x, helleste_stelle_y = max_loc

# Helligkeitswert der hellsten Stelle
helligkeitswert = max_wert

# Das Bild markieren, um die hellste Stelle zu zeigen (optional)
markiertes_bild = bild.copy()
cv2.circle(markiertes_bild, (helleste_stelle_x, helleste_stelle_y), 10, (0, 0, 255), 2)

# Das markierte Bild anzeigen
cv2.imshow('Markiertes Bild', markiertes_bild)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Ausgabe der Koordinaten und des Helligkeitswerts der hellsten Stelle
print(f'Hellste Stelle bei X: {helleste_stelle_x}, Y: {helleste_stelle_y}')
print(f'Helligkeitswert: {helligkeitswert}')

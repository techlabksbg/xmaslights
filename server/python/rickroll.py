import cv2
import numpy as np

cap= cv2.VideoCapture('testvideo.mp4')
success, image = cap.read()
count = 1
converted = []
values = []
ledValues = []
ledCoordinates = [line.split(' ') for line in open("3ddata.txt")]
ledCoordinates = [[float(i) for i in c]for c in ledCoordinates]
ledCoordinates = [[i+55 for i in c]for c in ledCoordinates]
ledCoordinates = [[round(i) for i in c]for c in ledCoordinates]
print(ledCoordinates)
f = f = open("ledData", "w")



print("I am in success")
while success:
  try:
    success,image = cap.read()
    resize = cv2.resize(image, (300, 300), interpolation = cv2.INTER_LINEAR) 
    converted.append(resize)
    cv2.imwrite("%03d.jpg", resize) # for debugging reasons
    c = 0
    for i in ledCoordinates:
        x = ledCoordinates[c]
        x = x[1]
        y = ledCoordinates[c]
        y = y[2]
        #print(x,y)
        v = (resize[x, y])
        #print("Pixel at (",x,",",y,") - Value ",v)
        #v = str(v)
        ledValues.append(v)
        c += 1


  except Exception as e:
    print("No value: ", str(e))
print("Conversion finished")

print(ledValues)
f.write(str(ledValues))

cap.release()
cv2.destroyAllWindows()


 
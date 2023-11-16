import cv2

cap= cv2.VideoCapture('automatic.mp4')
success, image = cap.read()
count = 0
converted = []
values = []
ledValues = []
ledCoordinates = [line.split(' ') for line in open("3ddata.txt")]
ledCoordinates = [[float(i) for i in c]for c in ledCoordinates]
print(ledCoordinates)


print("I am in success")
while success:
  try:
    success,image = cap.read()
    resize = cv2.resize(image, (40, 100), interpolation = cv2.INTER_LINEAR) 
    converted.append(resize)
    cv2.imwrite("%03d.jpg", resize) # for debugging reasons
    for x in range(40):
      for y in range(100):
        v = (resize[y, x])
        if ledCoordinates[count] >= [x-5,y-5,0,0] and ledCoordinates[count] <= [x+5,y+5,100,2]:
        #print("Pixel at ({}, {}) - Value {} ".format(x,y,v))
          ledValues[count] = (v)
          count += 1

        
  except Exception as e:
    print(str(e))
count = -1
print("Conversion finished")

cap.release()
cv2.destroyAllWindows()

print(ledValues)
 
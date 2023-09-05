import requests
import cv2
import os
import sleep from time
from datetime import datetime

LED_COUNT = 10

def init():
	cap = cv2.VideoCapture(0)
	temp = "temp"

	if not os.path.isdir(temp):
		print(f"Creating directory {temp}")
		os.mkdir("temp")
	
	subdir=temp+"/"+datetime.now().strftime("%Y%m%d_%H%M%S")

	print(f"Creating directory {subdir}")
	os.mkdir(subdir)
	return cap, subdir
	
	
def find_brightest_pixel(image):
	# Convert the image to grayscale for simplicity
	grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# Find the coordinates of the brightest pixel
	(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(grayscale_image)
	brightest_pixel = maxLoc
	brightness = maxVal

	return brightest_pixel, brightness

def get_image(dir, led):
	# Open the webcam
	ret, frame = cap.read()

	# save image to file into dir
	filename = f"{dir}/{led:04d}.png"
	# cv2.imshow(filename, frame)
	cv2.imwrite(filename, frame)

	# find brightest pixel and print it's coordinates and brightness
	brightest_pixel_coords, brightness_value = find_brightest_pixel(frame)
	print(led, ": ", brightest_pixel_coords, brightness_value, sep="")
	
def show_led(led):
	url = f"http://192.168.4.1/cmd?led={led}"
	r = requests.get(url, timeout=3)
	if(r.status_code != 200):
		print(f"Error: {r.status_code} when requesting {url}")
	sleep(0.5)

cap, subdir = init()
for led in range(LED_COUNT):
	show_led(led)
	get_image(subdir, led)
cap.release()
cv2.destroyAllWindows()

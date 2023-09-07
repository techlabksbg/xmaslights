import requests
import cv2
import os
from time import sleep
from datetime import datetime


LED_COUNT = 50


def init():
	# starting camera
	cap = cv2.VideoCapture(0)
	
	# creating directories
	temp = "temp"

	if not os.path.isdir(temp):
		print(f"Creating directory {temp}")
		os.mkdir(temp)
	
	subdir=temp+"/"+datetime.now().strftime("%Y%m%d_%H%M%S")


	print(f"Creating directory {subdir}")
	os.mkdir(subdir)
	
	return cap, subdir
	
def get_image(dir, led):
	# Open the webcam
	ret, frame = cap.read()


	# save image to file into dir
	filename = f"{dir}/{led:04d}.png"
	# cv2.imshow(filename, frame)
	cv2.imwrite(filename, frame)


def show_led(led):
	# turning on led
	url = f"http://192.168.4.1/cmd?led={led}"
	r = requests.get(url, timeout=3)


	if(r.status_code != 200):
		print(f"Error: {r.status_code} when requesting {url}")


cap, subdir = init()


for led in range(LED_COUNT):
	show_led(led)
	sleep(0.5)
	# get_image(subdir, led)


cap.release()
cv2.destroyAllWindows()


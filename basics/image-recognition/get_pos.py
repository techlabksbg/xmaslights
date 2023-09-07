import cv2
import os
import numpy as np

LED_COUNT = 50

def init():
	dir = "1st-try-sample-data/20230907_073717"
	return sorted([dir+"/"+f for f in os.listdir(dir)])
	
def find_brightest_pixel(image):
	grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert the image to grayscale for simplicity

	(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(grayscale_image)  # Find the coordinates of the brightest pixel
	brightest_pixel = maxLoc
	brightness = maxVal

	# find all the pixels coordinates with the brightest value
	brightest_pixels = np.argwhere(grayscale_image == maxVal)
	# return average of all the brightest pixels
	brightest_pixel = np.mean(brightest_pixels, axis=0, dtype=int)

	return (brightest_pixel[1], brightest_pixel[0]), brightness

def get_image(img):
	image = cv2.imread(img)
	led = img.split("/")[-1].split(".")[0]

	brightest_pixel, brightness = find_brightest_pixel(image)  # find lightest pixel in image
	cv2.circle(image, brightest_pixel, 5, (0, 0, 255), -1)  # Mark the brightest pixel with a red circle

	cv2.imshow("Image", image) # display image
	cv2.waitKey(500) # wait 500 ms

	print(f"LED {led} is at {brightest_pixel} with brightness {brightness}")

files = init()
for f in files:
	get_image(f)

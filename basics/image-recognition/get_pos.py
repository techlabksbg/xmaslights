import cv2
import os
import numpy as np

def init():
	dir = "1st-try-sample-data/20230907_073717"
	print("Loading images from", dir, "...")
	return sorted([dir+"/"+f for f in os.listdir(dir)])

def find_avg(image, col, pixel): # finds the average of col of a 10x10 square around the pixel
	return np.mean(image[pixel[1]-5:pixel[1]+5, pixel[0]-5:pixel[0]+5, col])
	
def find_brightest_pixel(image):
	grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert the image to grayscale for simplicity

	brightest_pixel = (-1, -1)
	red = 16
	green = 0
	blue = 0

	while red-blue > 15 and red-green > 15: # make sure the brightest pixel does not come from a red LED

		if (brightest_pixel[0] != -1):
			grayscale_image[brightest_pixel[1], brightest_pixel[0]] = 0 # set the brightest pixel to black so we don't find it again
		
		(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(grayscale_image)  # Find the coordinates of the brightest pixel
		brightest_pixel = maxLoc
		
		# find the average RGB values of a 10x10 square around the brightest pixel
		blue = find_avg(image, 0, brightest_pixel) 
		green = find_avg(image, 1, brightest_pixel)
		red = find_avg(image, 2, brightest_pixel)

	brightest_pixels = np.argwhere(grayscale_image == maxVal) # find all pixels with the same brightness
	brightest_pixel = np.median(brightest_pixels, axis=0) # take the mean of all the brightest pixels
	return (int(brightest_pixel[1]), int(brightest_pixel[0]))

def get_image(img):
	image = cv2.imread(img)
	led = img.split("/")[-1].split(".")[0]

	brightest_pixel = find_brightest_pixel(image)  # find lightest pixel in image
	cv2.circle(image, brightest_pixel, 5, (0, 0, 255), -1)  # mark the brightest pixel with a red circle

	cv2.imshow("Image", image) # display image
	cv2.waitKey(1000) # wait 500 ms

	print(f"LED {led}: {brightest_pixel}")

files = init()
for f in files:
	get_image(f)

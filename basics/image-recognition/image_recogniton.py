import cv2

# create new unique branch with your initials, like so
# git checkout -b ia_blc
#
# integrate 
#   web-request
#   creation of a directory in temp 
#   Saving images with filename %04d.png (LED-Number, 4 digits, leftpadded with zeros) into said directory
#
# move image recognition into a second program, reading images from a given directory.
#
# once everything works, make a pull request on GitHub.com
#

def find_brightest_pixel(image):
    # Convert the image to grayscale for simplicity
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Find the coordinates of the brightest pixel
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(grayscale_image)
    brightest_pixel = maxLoc
    brightness = maxVal

    return brightest_pixel, brightness


# Open the webcam
cap = cv2.VideoCapture(1)

while True:
    # Capture a frame from the webcam
    ret, frame = cap.read()

    if not ret:
        break

    # Find the brightest pixel in the frame
    brightest_pixel_coords, brightness_value = find_brightest_pixel(frame)

    # Draw a circle around the brightest pixel
    if brightest_pixel_coords:
        x, y = brightest_pixel_coords
        cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)  # Mark the brightest pixel with a red circle
        cv2.putText(frame, f"Brightness: {brightness_value}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display the frame
    cv2.imshow("Brightest Pixel Analysis", frame)
    print(brightest_pixel_coords, brightness_value)

    # Exit the loop when 'q' is pressed
    if cv2.waitKey(4) & 0xFF == ord('q'):
        break

# Release the webcam and close the display window
cap.release()
cv2.destroyAllWindows()

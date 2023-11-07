# Localization of LEDs in space

  * First, fix a coordinate system with (0,0,0) at the base of the trunk of your X-mas tree.
  * Position you camera and measure its 3D-coordinates. Also measure the heights of the lowest an highest LED.
  * Aquire the images running the ``01-aquire_images.py`` script.
  * Write the camera-coordinates and the LED-hights into the newly created directory (inside the temp directory) into a file called ``campos.txt`` in the following format

```txt
20 180 80
10 204
```

Repeat for at least one other position.

Then you can just run ``computeall.bash`` to analyze the images, project the LED-Coordinates into 3D-space and then determine the 3D-position.


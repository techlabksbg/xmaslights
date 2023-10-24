import numpy as np
import sys

def init():
    if len(sys.argv)!=2:
        print("Bitte einen Dateinamen angeben")
        quit()
    data = {}
    datei=sys.argv[1]
    if (datei[-4:]!='.txt'):
        print("Dateinamen muss mit .txt enden")
        quit()
    
    output = datei[0:-4]+"-projected.txt"

    with open(datei,"r") as f:
        cam = f.readline().split(' ')
        cam = np.array([float(c) for c in cam])
        heights = [int(h) for h in f.readline().split(' ')]
        indecies = [int(index) for index in f.readline().split(' ')]
        leds = f.readlines()
        leds = [[float(c) for c in x.split(' ')] for x in leds] 
        leds = [{'point':np.array(led[1:3]),'confidence':led[3]} for led in leds]
        data = {'cam': cam, 
                'heights':heights, 
                'height':heights[1]-heights[0],
                'indecies':indecies, # Tiefste und höchste LED-Nummer
                'leds':leds,
                'output':output}   # The file name to be used for the output
    return data

data = init()
bottom_n = data['indecies'][0]
top_n = data['indecies'][1]
numleds = len(data['leds'])

# S_1 S_2 in xyz und pq-Coordinates (image coordinates)
spq = (data['leds'][bottom_n]['point'],
       data['leds'][top_n]['point'])

# Camera position
kxyz = data['cam']
# Vector b
b = spq[1]-spq[0]
# Rotation about +90 degrees (from the image's x- to the  y-axis)
a = np.array([-b[1], b[0]])

# Matrix A (note: this is not a matrix-object, as its use is deprecated)
a = np.column_stack((a,b,spq[0]))  # No transpose needed this way
a = np.append(a,[[0,0,1]],axis=0)  # Add row matrix to the end

# All LEDs in pq-Coordinates
points = np.column_stack([p['point'] for p in data['leds']])
points = np.append(points, [np.ones(numleds)], axis=0)

# Projection plan vectors u and v
u = np.array([-kxyz[1], kxyz[0], 0]) #+90 degree rotation of cam vector
v = np.array([0,0,data['height']])  # straight up
u = u/np.linalg.norm(u)*data['height']  #adjust length

# Matrix B (again, not a matrix object)
b = np.column_stack((u,v,np.array([0,0,data['heights'][0]])))

# Final Transformation Matrix T (the '*' would be element-by-element multiplication, not matrix multiplication!)
#   (Alternatively one could use the '@'-operator to multiply matrices)
t = np.matmul(b, np.linalg.inv(a))

# Projected points
projected = np.matmul(t, points)

# Output
with open(data['output'], "w") as f:
    print("%.1f %.1f %.1f" % (kxyz[0], kxyz[1], kxyz[2]))
    f.write("%.1f %.1f %.1f\n" % (kxyz[0], kxyz[1], kxyz[2]))
    for i in range(numleds):
        print("%.1f %.1f %.1f %.3f" % (projected[0][i], projected[1][i], projected[2][i], data['leds'][i]['confidence']))
        f.write("%.1f %.1f %.1f %.3f\n" % (projected[0][i], projected[1][i], projected[2][i], data['leds'][i]['confidence']))

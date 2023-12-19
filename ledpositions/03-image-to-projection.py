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
    
    output = datei[0:-4]+".projected"

    with open(datei,"r") as f:
        cam = f.readline().split(' ')
        cam = np.array([float(c) for c in cam])
        heights = [float(h) for h in f.readline().split(' ')]
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
# Vector b in image coordinates
b = spq[1]-spq[0]
print(f"kxyz = {kxyz}")
camtree = np.linalg.norm(kxyz[0:2])  # Distance cam to tree (in cm)
print(f"camtree = {camtree}")
middleToTree = (data['leds'][bottom_n]['point'][0]-320)/np.linalg.norm(b)*data['height']  # Distance to image center in cm
print(f"bottom = {data['leds'][bottom_n]['point']}, middleToTree={middleToTree}")
hfp = middleToTree*middleToTree/camtree  # Distance to height onto camtree
h = (hfp*(camtree-hfp))**0.5   # Length of height to from camtree to image center
print(f"hfp = {hfp}, h={h}")
k = kxyz[0:2]
k /= np.linalg.norm(k)
kperp = np.array([-k[1], k[0]])
print(f"k={k}, kperp={kperp}")
if middleToTree>0:
    planex= -(k*hfp-h*kperp)
else:
    planex= k*hfp+h*kperp
planex *= data['height']/np.linalg.norm(planex)

# Rotation about +90 degrees (from the image's x- to the  y-axis)
a = np.array([-b[1], b[0]])

# Matrix A (note: this is not a matrix-object, as its use is deprecated)
a = np.column_stack((a,b,spq[0]))  # No transpose needed this way
a = np.append(a,[[0,0,1]],axis=0)  # Add row matrix to the end

# All LEDs in pq-Coordinates
points = np.column_stack([p['point'] for p in data['leds']])
points = np.append(points, [np.ones(numleds)], axis=0)

# Projection plan vectors u and v
# This only works, when the tree is centered on the image, otherwise, the plane is wrong.
u = np.array([-kxyz[1], kxyz[0], 0]) #+90 degree rotation of cam vector
u = u/np.linalg.norm(u)*data['height']  #adjust length
print(f"old u={u}")
#print(f"planex = {planex}")
u = np.array([planex[0], planex[1], 0])
print(f"new u = {u}")

v = np.array([0,0,data['height']])  # straight up

# Matrix B (again, not a matrix object)
b = np.column_stack((u,v,np.array([0,0,data['heights'][0]])))
print(f"a={a},\n b={b}")


# Final Transformation Matrix T (the '*' would be element-by-element multiplication, not matrix multiplication!)
#   (Alternatively one could use the '@'-operator to multiply matrices)
t = np.matmul(b, np.linalg.inv(a))

print(f"t = {t}")

# Projected points
projected = np.matmul(t, points)


# Output
with open(data['output'], "w") as f:
    #print("%.1f %.1f %.1f" % (kxyz[0], kxyz[1], kxyz[2]))
    f.write("%.1f %.1f %.1f\n" % (kxyz[0], kxyz[1], kxyz[2]))
    for i in range(numleds):
        #print("%.1f %.1f %.1f %.3f" % (projected[0][i], projected[1][i], projected[2][i], data['leds'][i]['confidence']))
        f.write("%.1f %.1f %.1f %.3f\n" % (projected[0][i], projected[1][i], projected[2][i], data['leds'][i]['confidence']))

#!/usr/bin/python3

import numpy as np

with open("3ddata.txt", "r") as f:
    points = np.column_stack([[float(c) for c in l.split(" ")][0:3] for l in f.readlines()])

n = points.shape[1]

for i in range(5):
    dists = [np.linalg.norm(points[:,i+1] - points[:,i]) for i in range(n-1)]
    distoff = [abs(10-dists[i-1])+abs(10-dists[i])+abs(20-dists[i-1]-dists[i]) for i in range(1,n-1)]

    print(f"max dists={max(dists)}, max distoff={max(distoff)}")

    for i in range(n-2):
        if distoff[i]>20:
            points[:,i+1]=0.5*(points[:,i]+points[:,i+2])


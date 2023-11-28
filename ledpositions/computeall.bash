#!/bin/bash

for dir in temp/*
do
    if test -d $dir; then
        echo "Analyzing images in $dir, generating $dir.txt"
        python3 02-analyze_images.py $dir > $dir.txt
    fi
done

for txt in temp/*.txt
do
    echo "Projecting coordinates from $txt"
    python3 03-image-to-projection.py $txt > /dev/null
done

echo "Intersecting lines... from " temp/*.projected 
python3 04-approximate-line-intersection.py temp/*.projected > 3ddata.txt

echo "saved 3D-Data in 3ddata.txt"

python3 05-clean-improbable-positions.py

echo "Saved cleaned data in cleaned.txt"
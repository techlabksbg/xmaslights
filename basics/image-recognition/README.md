# Installation

```bash
pip install python-opencv
pip install requests
```

## Aquire images
```bash
python3 aquire_images.py 
```

## Analyze images (generate image coordinates of leds)
```
python3 analyze_image.py temp/20230101_123456/ > data1.txt
```

oder alle auf einmal generieren
```bash
cd temp
for a in *
do
   python3 ../analyze_image.py $a > $a.txt
done
```

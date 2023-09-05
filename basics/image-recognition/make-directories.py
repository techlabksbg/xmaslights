import os
from datetime import datetime

temp = "temp"

if not os.path.isdir(temp):
    print(f"Creating directory {temp}")
    os.mkdir("temp")


subdir=temp+"/"+datetime.now().strftime("%Y%m%d_%H%M%S")

print(f"Creating directory {subdir}")
os.mkdir(subdir)





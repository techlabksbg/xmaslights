# See also: https://stackoverflow.com/questions/17178483/how-do-you-send-an-http-get-web-request-in-python

import requests
import time


for led in range(50):
    url = f"http://192.168.4.1/cmd?led={led}"
    print(url)
    r = requests.get(url, timeout=3)
    print(r.status_code)     # Sollte 200 sein (HTTP OK)
    sleep(0.5)



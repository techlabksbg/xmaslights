from UDPServer import UDP_Server
from leds import LEDs
from example import Example
import time


server = UDP_Server()
leds = LEDs(30)
example = Example()

start = time.time()
nextTime = start+5
f = 0
while True:
    stop = time.time()+0.01
    while time.time()<stop:
        server.loop()
    example.step(leds)
    f+=1
    if time.time()>nextTime:
        nextTime = time.time()+5
        t = time.time()-start
        fps = f/t
        print("%d f in %.1f secs: %.1f fps" % (f, t, fps))
    if leds.changed:
        server.send(leds.bin())



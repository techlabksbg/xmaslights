from UDPServer import UDP_Server
from leds import LEDs
from example import Example
import time
from httpServer import httpServer


config = {'configChanged':False}   # empty Dict, will be set by httpServer

http = httpServer(config)  # Start and run http server

server = UDP_Server()
leds = LEDs(200)
example = Example()

start = time.time()
nextTime = start+5
f = 0
while True:
    stop = time.time()+0.01
    while time.time()<stop:
        time.sleep(0.001)
        server.loop()
    if config['configChanged']:  # This is a race condition, might change
        example.setConfig(config)
        config['configChanged']=False
    example.step(leds)
    f+=1
    if time.time()>nextTime:
        nextTime = time.time()+5
        t = time.time()-start
        fps = f/t
        print("%d f in %.1f secs: %.1f fps" % (f, t, fps))
    if leds.changed:
        server.send(leds.bin())



from UDPServer import UDP_Server
from leds import LEDs
import time
from httpServer import httpServer
import numpy as np
from config import Config

config = Config()
config.registerKey('brightness', {'type':float, 'low':0.01, 'high':1.0, 'default':0.2})
config.registerKey('saturation', {'type':float, 'low':0.0, 'high':1.0, 'default':1.0})
config.registerKey('period', {'type':float, 'low':1, 'high':20, 'default':5})
config.registerKey('color', {'type':'color', 'default':[255,255,255]})


http = httpServer(config)  # Start and run http server

server = UDP_Server()  # Start udp server (will run on the main thread)

with open("3ddata.txt", "r") as f:
    points = np.column_stack([[float(c) for c in l.split(" ")][0:3] for l in f.readlines()])

leds = LEDs(800, (1,0,2))  # GRB color order

programNames = ["Example", "SingleLED", "Rainbow3d", "Kugeln","spiral"]
config.registerKey('prg', {'type':str, 'default':'spiral', 'allowed':programNames, 'minage':3})  # At lest 3 secs since last request to change this setting.
modules = [__import__(m.lower()) for m in programNames]
programs = {programNames[i]:getattr(m, programNames[i])(config) for i,m in enumerate(modules)}


start = time.time()
nextTime = start+5
f = 0
while True:
    stop = time.time()+0.016
    while time.time()<stop:
        time.sleep(0.001)
        server.loop()
    programs[config['prg']].step(leds, points)

    if leds.changed:
        clientPresent = server.send(leds.bin())
        if (clientPresent):
            f+=1
        else:
            f = 0
            start = time.time()

    if time.time()>nextTime:
        nextTime = time.time()+5
        t = time.time()-start
        if t>0:
            fps = f/t
            print("[%s] %d frames in %.1f secs: %.1f fps, %s" % (config['prg'], f, t, fps, "connected" if clientPresent else "not connected"))
        else:
            print("No connection")



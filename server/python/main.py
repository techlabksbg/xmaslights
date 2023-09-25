from UDPServer import UDP_Server
from leds import LEDs
import time
from httpServer import httpServer
import importlib


config = {'configChanged':False}   # dictionary, will be set by httpServer, read by programs

http = httpServer(config)  # Start and run http server

server = UDP_Server()  # Start udp server (will run on the main thread)

leds = LEDs(200, (1,0,2))  # GRB color order

programNames = ["Example", "SingleLED"]
modules = [__import__(m.lower()) for m in programNames]
programs = {programNames[i]:getattr(m, programNames[i])() for i,m in enumerate(modules)}

activeProgram = "Example"

start = time.time()
nextTime = start+5
f = 0
while True:
    stop = time.time()+0.01
    while time.time()<stop:
        time.sleep(0.001)
        server.loop()
    if config['configChanged']:  # This is a race condition, might change, use semaphores?
        if 'activeProgram' in config  and config['activeProgram'] in programs:
            activeProgram = config['activeProgram']
        del config['activeProgram']
        programs[activeProgram].setConfig(config)
        config['configChanged']=False
    programs[activeProgram].step(leds)
    if leds.changed:
        server.send(leds.bin())
    
    f+=1
    if time.time()>nextTime:
        nextTime = time.time()+5
        t = time.time()-start
        fps = f/t
        print("[%s] %d f in %.1f secs: %.1f fps" % (activeProgram, f, t, fps))



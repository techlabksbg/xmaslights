# The Xmaslights Server
# Starts a UDP Server on Port 15878 for the LED-Data
# Starts a Webserver on Port 15878
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

    def startServers(self):
        self.http = httpServer(self.config)  # Start and run http server
        self.udp = UDP_Server()  # Init udp server (will run on the main thread)

    def get3dData(self):
        with open("3ddata.txt", "r") as f:
            self.points = np.column_stack([[float(c) for c in l.split(" ")][0:3] for l in f.readlines()])

leds = LEDs(800, (1,0,2))  # GRB color order

programNames = ["Example", "SingleLED", "Rainbow3d", "Kugeln"]
config.registerKey('prg', {'type':str, 'default':'Example', 'allowed':programNames, 'minage':3})  # At lest 3 secs since last request to change this setting.
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


    def debug(self):
        self.nextTime = time.time()+60
        t = time.time()-self.start
        if t>0:
            fps = self.frames/t
            logger.info("[%s] %d frames in %.1f secs: %.1f fps, %s, since motion: %f" % (self.config['prg'], self.frames, t, fps, "connected" if self.clientPresent else "not connected", time.time()-self.udp.motionDetected))
        else:
            logger.info("No connection")

    def programSwitcher(self):
        if self.config.changed:
            self.programStart = self.config.lastChange
        if self.timeControl.powerMode()=="on" or time.time()-self.udp.motionDetected<60:
            autoswitch = False
            currentDefaults = self.programs[self.activeProgram].defaults()
            triggered = self.timeControl.getTriggeredEvents()
            if len(triggered)>0:
                autoswitch = triggered[-1]
                logger.info(f"timeControl triggered {autoswitch}")
            elif self.activeProgram!=self.config['prg']:
                logger.info(f"Config switch to {self.config['prg']}")
                autoswitch = self.config['prg']
            elif 'playFor' in currentDefaults and time.time()>self.programStart+currentDefaults['playFor'] or \
                    self.activeProgram=="Standby" or time.time() - self.programStart>120:  # Max 2 min autoplay
                i = (self.programNames.index(self.activeProgram)+1)%len(self.programNames)
                while not 'autoPlay' in self.programs[self.programNames[i]].defaults() or \
                            not self.programs[self.programNames[i]].defaults()['autoPlay']:
                    i = (i+1)%len(self.programNames)
                autoswitch = self.programNames[i]
            
            if autoswitch and autoswitch!=self.activeProgram:
                logger.info(f"Switch to {autoswitch}")
                self.config.parsePair('prg', autoswitch,99999)
                self.activeProgram = autoswitch
                self.programStart = time.time()
                # Set default values on autoplay
                defaults = self.programs[self.activeProgram].defaults()
                if 'params' in defaults:
                    for key,value in defaults['params'].items():
                        self.config.parsePair(key, value, 9999)
        else:
            self.activeProgram = "Standby"
            self.config.parsePair('prg', self.activeProgram,99999)
            self.programStart = time.time()
        self.config.changed = False
        

    def run(self):
        # Read params from myconfig.txt (if it exists)
        self.config.loadDefaults()
        self.start = time.time()
        self.nextTime = self.start+5
        self.frames = 0
        self.activeProgram = self.config['prg']
        self.programStart = time.time()

        fileWatcher = FileWatcher()
        nextFileWatcher = time.time()+1
        while self.http.thread.is_alive:  # Exit program if http server crashes
            self.step()
            self.programSwitcher() 
            if time.time()>nextFileWatcher:
                nextFileWatcher = time.time()+1
                if fileWatcher.new_files():
                    logger.warn("New files detected, stopping server")
                    exit(0)
            if time.time()>self.nextTime:
                self.debug()


XmaslightsServer().run()

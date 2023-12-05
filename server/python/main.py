# The Xmaslights Server
# Starts a UDP Server on Port 15878 for the LED-Data
# Starts a Webserver on Port 15878
from UDPServer import UDP_Server
from leds import LEDs
import time
from httpServer import httpServer
import numpy as np
from config import Config
from filewatcher import FileWatcher
from timecontrol import TimeControl
import sys
import glob
import inspect
from logger import logger

class XmaslightsServer():
    def __init__(self):
        self.leds = LEDs(800, (1,0,2))  # GRB color order
        
        self.initConfig()
        self.initTimeControl()
        self.startServers()
        self.get3dData()
        self.importPrograms()

    def initTimeControl(self):
        self.timeControl = TimeControl()
        self.config.setTimeControl(self.timeControl)
    
    def initConfig(self):
        self.config = Config()
        self.config.registerKey('brightness', {'type':float, 'low':0.01, 'high':1.0, 'default':0.2})
        self.config.registerKey('saturation', {'type':float, 'low':0.0, 'high':1.0, 'default':1.0})
        self.config.registerKey('period', {'type':float, 'low':1, 'high':20, 'default':5})
        self.config.registerKey('color', {'type':'color', 'default':[255,0,0]})
        self.config.registerKey('color2', {'type':'color', 'default':[0,255,0]})

    def startServers(self):
        self.http = httpServer(self.config)  # Start and run http server
        self.udp = UDP_Server()  # Init udp server (will run on the main thread)

    def get3dData(self):
        with open("3ddata.txt", "r") as f:
            self.points = np.column_stack([[float(c) for c in l.split(" ")][0:3] for l in f.readlines()])

    def importPrograms(self):
        # Get enabled animations
        enabled = [f[19:-3] for f in glob.glob("animations_enabled/*.py")]
        # Allow direct imports from animations_availabe
        sys.path.append("animations_available")
        # Import all modules
        modules = [__import__(f) for f in enabled]
        # Extract classnames and classes from imported modules
        classinfo = [[info for info in inspect.getmembers(m, inspect.isclass) if info[0]!="LEDs" and info[0]!="Program"][0] for m in modules]
        # Names of classes
        self.programNames = [info[0] for info in classinfo]
        # Create instances of each class
        self.programs = {info[0] : info[1](self.config) for info in classinfo}
        # Get the first autoplaying program and set it as default
        active = 0
        while (not 'autoPlay' in self.programs[self.programNames[active]].defaults()):
            active+=1
        # Register enabled programs in config
        self.config.registerKey('prg', {'type':str, 'default':self.programNames[active], 'allowed':self.programNames, 'minage':0.3})  # At lest 3 secs since last request to change this setting.
        # Build WebConfig
        for name, prg in self.programs.items():
            d = prg.defaults()
            if 'web' in d and d['web']:
                self.config.webconfig[name] = list(d['params'].keys())
    


    def step(self):
        # Wait and receive UPD packets
        stop = time.time()+0.016
        while time.time()<stop:
            time.sleep(0.001)
            self.udp.loop()
        # Compute new frame
        self.programs[self.activeProgram].step(self.leds, self.points)
        # Send frame if changes were made
        if self.leds.changed:
            self.clientPresent = self.udp.send(self.leds.bin())
            if (self.clientPresent):
                self.frames+=1
            else:
                self.frames = 0
                self.start = time.time()


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
        if self.timeControl.powerMode()=="on" or time.time()-self.udp.motionDetected<120 or time.time()-self.config.lastHttpRequest<120:
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

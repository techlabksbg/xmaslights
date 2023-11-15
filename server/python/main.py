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

class XmaslightsServer():
    def __init__(self):
        self.leds = LEDs(800, (1,0,2))  # GRB color order
        
        self.initConfig()
        self.startServers()
        self.get3dData()
        self.importPrograms()
        self.initTimeControl()

    def initTimeControl(self):
        self.timeControl = TimeControl()
    
    def initConfig(self):
        self.config = Config()
        self.config.registerKey('brightness', {'type':float, 'low':0.01, 'high':1.0, 'default':0.2})
        self.config.registerKey('saturation', {'type':float, 'low':0.0, 'high':1.0, 'default':1.0})
        self.config.registerKey('period', {'type':float, 'low':1, 'high':20, 'default':5})
        self.config.registerKey('color', {'type':'color', 'default':[255,255,255]})

    def startServers(self):
        self.http = httpServer(self.config)  # Start and run http server
        self.udp = UDP_Server()  # Init udp server (will run on the main thread)

    def get3dData(self):
        with open("3ddata.txt", "r") as f:
            self.points = np.column_stack([[float(c) for c in l.split(" ")][0:3] for l in f.readlines()])

    def importPrograms(self):
        # Get enabled animations
        enabled = [f[0:-3] for f in glob.glob("*.py", root_dir="animations_enabled")]
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
        while (not 'autoplay' in self.programs[self.programNames[active]].defaults()):
            active+=1
        # Register enabled programs in config
        self.config.registerKey('prg', {'type':str, 'default':self.programNames[active], 'allowed':self.programNames, 'minage':0.3})  # At lest 3 secs since last request to change this setting.

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
        self.nextTime = time.time()+5
        t = time.time()-self.start
        if t>0:
            fps = self.frames/t
            print("[%s] %d frames in %.1f secs: %.1f fps, %s" % (self.config['prg'], self.frames, t, fps, "connected" if self.clientPresent else "not connected"))
        else:
            print("No connection")

    def programSwitcher(self):
        if self.config.changed:
            self.programStart = time.time()
        if self.timeControl.powerMode()=="on":
            if self.activeProgram!=self.config['prg']:
                self.activeProgram = self.config['prg']
                self.programStart = time.time()
            defaults = self.programs[self.activeProgram].defaults()
            if 'autoplay' in defaults and time.time()>self.programStart+defaults['autoplay']:
                i = (self.programNames.index(self.activeProgram)+1)%len(self.programNames)
                while not 'autoplay' in self.programs[self.programNames[i]].defaults():
                    i = (i+1)%len(self.programNames)
                self.activeProgram = self.programNames[i]
                self.config.parsePair('prg', self.activeProgram,99999)
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

        while self.http.thread.is_alive:  # Exit program if http server crashes
            self.step()
            self.programSwitcher() 
            if time.time()>self.nextTime:
                self.debug()
                if fileWatcher.new_files():
                    print("New files detected, stopping server")
                    exit(0)


XmaslightsServer().run()

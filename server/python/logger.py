from datetime import datetime
import inspect
import os
import sys

class Logger:
    def __init__(self, levels=["error", "warn", "info"]):
        if not os.path.exists("logs"):
            os.mkdir("logs")
        self.filename = f"logs/xmaslights-{datetime.now().isoformat()}.log"
        self.file = open(self.filename, "w")
        sys.stderr = self.file
        self.levels=levels
        self.info("Logger started")

    def log(self, str, tag=""):
        if (len(tag)>0 and tag[-1]!=" "):
            tag+=" "
        curframe = inspect.currentframe()
        callframe = inspect.getouterframes(curframe, 2)
        filename = os.path.basename(callframe[2].filename)
        lineno = callframe[2].lineno
        fct = callframe[2].function
        tstamp = datetime.now().isoformat()
        logstr = f"{tstamp} {tag}[{filename}:{lineno}] in {fct}: {str}"
        print(logstr)
        self.file.write(logstr+"\n")
        del curframe
        del callframe
    
    def error(self, str):
        self.log(str, "error")
    
    def warn(self, str):
        self.log(str, "warn")
    
    def debug(self, str):
        self.log(str, "debug")
    
    def info(self, str):
        self.log(str, "info")
    

logger = Logger()
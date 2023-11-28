import datetime

class TimeControl:
    def __init__(self):
        self.events = []
        self.triggered = ""
        self.lastCheck = datetime.datetime.now()

    def registerEvent(self, event):
        self.events.append(event)

    def isHot(self, event, dt):
        if 'at' in event:
           return dt.hour==event['at']['h'] and dt.minute==event['at']['m']

        if 'every' in event:
            offset = 0
            if 'offset' in event['every']:
                offset = event['every']['offset']
            return (dt.second+dt.minute*60) % event['every']['s'] == offset
        
        return False



    def atTime(self, h,m, prg):
        self.registerEvent({'at':{'h':h, 'm':m}, 'prg':prg})

    def every(self, seconds, offset, prg):
        self.registerEvent({'every':{'s': seconds, 'offset':offset}, 'prg':prg})
        
    def getTriggeredEvents(self):
        t = datetime.datetime.now()
        prgs = [e['prg'] for e in self.events if ((not self.isHot(e,self.lastCheck)) and self.isHot(e, t))]
        self.lastCheck = t
        if (len(prgs)>0):
            print(f"triggered {prgs} at {t}")
        return prgs

    def powerMode(self):
        t = datetime.datetime.now()
        if (t.hour>=19 or t.hour<7 or t.weekday==6): 
            return "off"
        return "on"
    

        
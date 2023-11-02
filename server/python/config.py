

class Config:
    def __init__(self):
        self.config={}
        self.keys={}

    def __getitem__(self, key):        
        return self.config[key]
    
    def clamp(self, value, params):
        if (value<params["low"]):
            return params["low"]
        if (value>params["high"]):
            return params["high"]
        return value
    
    def checkType(self, text, params):
        try:
            f = params["type"](text)
            return self.clamp(f, params)
        except ValueError:
            return params["old"]
        
    def checkHexColor(self, text, params):
        if len(text)==6:
            try:
                c = list((int(text[i:i+2],16) for i in range(0,6,2)))
                return c
            except ValueError:
                pass
        return params['old']

    def checkArray(self,text, params):
        a = text.split(",")
        if len(a)!=params["len"]:
            return params['old']
        old = params['old']

        for i in range(len(a)):
            params['old']=None
            a[i] = self.checkType(a[i], params)
            if a[i]==None:
                params['old']=old
                return old
        params['old']=old
        return a

    def checkString(self, text, params):
        if 'allowed' in params:
            if text in params['allowed']:
                return text
            else:
                return params['old']
        
        if 'maxlen' in params and len(text)>params['maxlen']:
            return params['old']
            
        if 'minlen' in params and len(text)<params['minlen']:
            return params['old']
        
        return text
        
        
    def registerKey(self, key, params):
        print(f"Registered key {key} with params #{params} ")
        self.keys[key] = params
        self.config[key]=params['default']

    def parsePair(self, key, value):
        if key in self.keys:
            # Prepare default value
            if key in self.config:
                self.keys[key]['old'] = self.config[key]
            elif 'default' in self.keys[key]:
                self.keys[key]['old'] = self.keys[key]['default']
            
            # Is it an array?
            if 'array' in self.keys[key] and self.keys[key]['array']:
                self.config[key] = self.checkArray(value, self.keys[key])
                return
            
            if self.keys[key]['type'] in [float, int]:
                self.config[key] = self.checkType(value, self.keys[key])
                return

            if self.keys[key]['type']==str:
                self.config[key] = self.checkString(value, self.keys[key])
                return

            if self.keys[key]['type']=='color':
                self.config[key] = self.checkHexColor(value, self.keys[key])
                return

            raise NotImplementedError("Bad config params: #{self.keys[key]}")
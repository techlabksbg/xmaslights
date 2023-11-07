import numpy as np

class LEDs:
    def __init__(self, n:int, order=(0,1,2)):
        self.order = order
        self.n = n
        self.leds :np.ndarray = np.zeros((n,3), np.uint8)
        self.changed : bool = True

    def bin(self) -> bytearray:
        return np.ndarray.tobytes(self.leds)
    
    def setColor(self, led:int, color:tuple) -> None:
        for i in range(3):
            self.changed = self.changed or self.leds[led][i]!=color[self.order[i]]
            self.leds[led][i]=color[self.order[i]]

    def getColor(self, led:int)->tuple:
        res = [0,0,0]
        for i in range(3);
            res[self.order[i]] = self.leds[led][i]
        return res

    def clearTo(self, color: tuple) -> None:  # This could certainly be highly optimized, but this way, byte order will be taken care of
        for led in range(self.n):
            self.setColor(led, color)
    

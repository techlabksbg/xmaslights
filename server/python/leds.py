import numpy as np

class LEDs:
    def __init__(self,n:int):
        self.n = n
        self.leds :np.ndarray = np.zeros((n,3), np.uint8)
        self.changed : bool = True

    def bin(self) -> bytearray:
        return np.ndarray.tobytes(self.leds)
    
    def setColor(self, led:int, color:tuple) -> None:
        for i in range(3):
            self.changed = self.changed or self.leds[led][i]!=color[i]
            self.leds[led][i]=color[i]

    def clearTo(self, color: tuple) -> None:  # This could certainly be highly optimized
        for led in range(self.n):
            self.setColor(led, color)
    

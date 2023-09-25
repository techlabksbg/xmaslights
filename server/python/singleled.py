from program import Programm
from leds import LEDs


class SingleLED(Programm):

    def __init__(self):
        self.led = -1
        self.color = (255,255,255)

    def step(self, leds:LEDs) -> None:
        leds.clearTo((0,0,0))
        if (self.led>=0 and self.led<leds.n):            
            leds.setColor(self.led, self.color)

    def setConfig(self, config: dict) -> None:
        if 'led' in config:
            try:
                self.led = int(config['led'])
                print(f"Set LED to #{self.led}")
            except ValueError:
                pass

        if 'color' in config:
            if len(config['color'])==6:  # HEXvalues
                try:
                    c = list((int(config['color'][i:i+2],16) for i in range(0,6,2)))
                    self.color = c
                    print(f"set color to {c}")
                except ValueError:
                    pass
            
from program import Programm
from leds import LEDs


class singleLED(Programm):
    def step(self, leds:LEDs) -> None:
        leds.clearTo((0,0,0))
        if "led" in self.params and "color" in self.params:
            leds.setColor(self.params["led"], self.params["color"])

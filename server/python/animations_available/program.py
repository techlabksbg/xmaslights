from leds import LEDs

class Program:
    def __init__(self, config):
        self.config = config

    def step(self, leds:LEDs, points=None) -> None:
        pass

    def defaults(self):
        return {'params':{'brightness':0.1, 'saturation':1.0, 'period':10}}
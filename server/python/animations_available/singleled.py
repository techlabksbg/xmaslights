from program import Program
from leds import LEDs


class SingleLED(Program):

    def __init__(self, config):
        self.config = config
        config.registerKey('led', {'type':int, 'low':-1, 'high':799, 'default':0})

    def step(self, leds:LEDs, points=None) -> None:
        leds.clearTo((0,0,0))
        if (self.config['led']>=0 and self.config['led']<leds.n):
            leds.setColor(self.config['led'], self.config['color'])

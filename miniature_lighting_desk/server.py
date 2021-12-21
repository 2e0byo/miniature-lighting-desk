import json

from . import async_hal as hal


class Server:
    """Server controlling a miniature lighting controller."""

    def __init__(self, channels: int = 8):
        self.controller = hal.Controller()
        self.channels = [hal.Channel(self.controller, i) for i in range(channels)]
        self.vals = []
        self.sync()

    def set(self, channel: int, val: int):
        if self.vals[channel] != val:
            self.channels[channel].set_brightness(val)
        self.vals[channel] = val

    def get(self, channel: int):
        return self.vals[channel]

    def sync(self):
        self.vals = [channel.get_brightness() for channel in self.channels]

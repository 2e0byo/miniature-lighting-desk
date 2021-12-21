import asyncio
from functools import partial
from re import search
from threading import Thread
from time import sleep

import usb


class ControllerError(Exception):
    """Controller failed to respond correctly after retries."""


class Controller:
    """
    (Semi) Asynchronous class to represent a controller.

    Note that we do block, we just await between writes.
    """

    def __init__(self, timeout=100):
        VENDOR = 0x04D8
        PRODUCT = 0xFEAA
        CONFIGURATION = 0x01
        self._start_async()
        # find pinguino
        pinguino = None
        for bus in usb.busses():
            for dev in bus.devices:
                if dev.idVendor == VENDOR and dev.idProduct == PRODUCT:
                    pinguino = dev
        if not pinguino:
            raise ControllerError("No Controller Found!")
        self.dh = pinguino.open()
        self.dh.setConfiguration(CONFIGURATION)
        self.dh.claimInterface(0)
        self.retries = 2
        self.timeout = timeout

    def _start_async(self):
        """Start an asyncio loop in the background."""
        self.loop = asyncio.new_event_loop()
        t = Thread(target=self.loop.run_forever)
        t.daemon = True
        t.start()

    def stop_async(self):
        """Stop background asyncio loop."""
        self.loop.call_soon_threadsafe(self.loop.stop)

    def submit_async(self, awaitable):
        """Submit an awaitable to the background asyncio loop, returning a future for
        it."""
        return asyncio.run_coroutine_threadsafe(awaitable(), self.loop)

    def _read(self, length):
        ENDPOINT_IN = 0x81
        buf = self.dh.bulkRead(ENDPOINT_IN, length, self.timeout)
        return "".join([chr(i) for i in buf])

    def _write(self, buf):
        ENDPOINT_OUT = 0x01
        return self.dh.bulkWrite(ENDPOINT_OUT, buf.encode(), self.timeout)

    def send(self, msg: str):
        for i in range(self.retries):
            self._write(msg)
            ret = self._read(64)
            if "Error" not in ret:
                return ret
        raise ControllerError(ret)

    async def __await__set_brightness(self, channel, brightness, pause=0):
        msg = f"s{channel}{brightness:03d}"
        ret = self.send(msg)
        await asyncio.sleep(pause)
        return ret

    async def __await__get_brightness(self, channel):
        msg = f"g{channel:01d}"
        ret = self.send(msg)
        await asyncio.sleep(0)
        return ret

    async def __await__fade_brightness(self, channel, start, end, fade_time):
        steps = abs(end - start)
        pause = fade_time / steps
        if end > start:
            steps = range(start, end + 1)
        else:
            steps = range(start, end - 1, -1)
        for step in steps:
            await self.__await__set_brightness(channel, 256 - step, pause)
            start = 256 - step

    def fade_brightness(self, channel, start, end, fade_time):
        """Queue fading control."""
        return self.submit_async(
            partial(self.__await__fade_brightness, channel, start, end, fade_time)
        )

    def set_brightness(self, channel, brightness, pause=0):
        """Queue setting brightness."""
        brightness = 256 - brightness
        return self.submit_async(
            partial(self.__await__set_brightness, channel, brightness, pause)
        )

    def get_brightness(self, channel, pause=0):
        """Queue getting brightness."""
        future = self.submit_async(partial(self.__await__get_brightness, channel))
        while not future.done():
            sleep(0.0001)  # wait in case we queue
        match = search(r"Channel ([0-9]) is ([0-9]+)", future.result())
        if not match:
            raise ControllerError(f"Garbage returned: {future.result()}")
        chan, brightness = match.groups()
        if int(chan) == channel:
            return 256 - int(brightness)
        else:
            raise ControllerError("Wrong channel returned!")


class Channel:
    """Class to represent a particular channel on the controller."""

    def __init__(
        self,
        controller: Controller,
        channel_number,
        on_brightness=256,
        off_brightness=0,
    ):
        self.controller = controller
        self.channel_number = channel_number
        self._query()  # get brightness
        self.on_brightness = on_brightness
        self.off_brightness = off_brightness

    def _query(self):
        """Get current value from controller."""
        self.value = self.controller.get_brightness(self.channel_number)

    def _set_value(self):
        """Write value for channel to controller."""
        return self.controller.set_brightness(self.channel_number, self.value)

    def set_brightness(self, brightness):
        """Brightness is an integer between 0 and 256."""
        self.value = brightness
        self._set_value()

    def get_brightness(self):
        """Get brightness for channel as an integer between 0 and 255."""
        return self.value

    def set_percent_brightness(self, brightness):
        """Set brightness for channel as a percentage, represented by a float between 0
        and 1."""
        self.value = round(brightness * 256)
        self._set_value()

    def get_percent_brightness(self):
        """Get brightness for channel as a percentage, represented by a float between 0
        and 1."""
        return self.value / 255

    def fade_on(self, fade_time=1):
        """
        Fade on in fade_time seconds.

        Note that the channel thinks this is atomic, i.e. it has no idea
        of the actual brightness during the fade (although cancelling
        will query the controller for it.)
        """

        self.fade_future = self.controller.fade_brightness(
            self.channel_number, self.value, self.on_brightness, fade_time
        )
        self.value = self.on_brightness

    def fade_off(self, fade_time=1):
        """
        Fade off in fade_time seconds.

        Note that the channel thinks this is atomic, i.e. it has no idea
        of the actual brightness during the fade (although cancelling
        will query the controller for it.)
        """
        self.fade_future = self.controller.fade_brightness(
            self.channel_number, self.value, self.off_brightness, fade_time
        )
        self.value = self.off_brightness

    def cancel_fade(self):
        """Cancel ongoing fade and then query controller for actual channel value."""
        self.fade_future.cancel()
        self._query()


if __name__ == "__main__":
    # for testing or example
    cont = Controller()
    green = Channel(cont, 7)
    red = Channel(cont, 0)

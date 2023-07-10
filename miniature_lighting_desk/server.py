import asyncio
from logging import getLogger
from unittest.mock import MagicMock

from autobahn.asyncio.component import Component, run

from . import async_hal as hal


class Timer:
    def __init__(self, func, delay_ms: int):
        self._func = func
        self._delay_ms = int(delay_ms / 100)
        self.remaining_ms = self._delay_ms
        self.running = False
        self._started = False

    async def start(self):
        self.running = True
        if not self._started:
            asyncio.create_task(self._loop())

    async def stop(self):
        self.running = False

    async def reset(self):
        self.remaining_ms = self._delay_ms

    async def _loop(self):
        while True:
            while self.running:
                await asyncio.sleep(0.1)
                self.remaining_ms -= 1
                if self.remaining_ms == 0:
                    await self._func()
                    break
            await self.stop()
            await self.reset()

            while not self.running:
                await asyncio.sleep(0.1)


class Backend:
    """Backend controlling a miniature lighting controller."""

    instances = []

    def __init__(
        self,
        *,
        component: Component,
        controller: hal.ControllerABC,
        channel=None,
    ):
        self.name = f"ControllerServer-{len(self.instances)}"
        self.instances.append(self.name)
        self._logger = getLogger(self.name)

        self.controller = controller
        channel = channel or hal.Channel
        self.channels = [
            channel(self.controller, i) for i in range(controller.no_channels)
        ]
        self.vals = []
        self.sync()
        self.component = component
        component.on_join(self.join)
        self.timer = Timer(self.publish, 5_000)

        component.register("sync")(self.sync)
        component.register("get_brightness")(self.get_brightness)
        component.register("set_brightness")(self.set_brightness)
        component.register("details")(self.details)

    def run(self):
        run([self.component])

    def join(self, session, details):
        self.session = session
        self._logger.info(f"Joined {session} {details}")

    async def ping(self):
        return "hello"

    async def details(self):
        return dict(
            channels=len(self.vals),
            name=self.name,
            vals=self.vals,
            max_brightness=self.controller.max_brightness,
        )

    async def set_brightness(self, *, channel: int, val: int):
        if self.vals[channel] != val:
            await self.timer.reset()
            await self.timer.start()
            self._logger.info(f"Setting channel {channel} to val {val}")
            self.channels[channel].set_brightness(val)
            self.vals[channel] = val

    async def publish(self):
        self._logger.info("Publishing statechange")
        self.session.publish("controller.statechange", self.vals)

    async def get_brightness(self, *, channel: int):
        self._logger.debug(f"Got {self.vals[channel]} for channel {channel}")
        return self.vals[channel]

    def sync(self):
        self.vals = [channel.get_brightness() for channel in self.channels]


# class MockBackend(Backend):
#     """A backend with the hardware mocked away."""

#     def __init__(
#         self,
#         **kwargs,
#     ):
#         kwargs["channel"] = MockChannel
#         kwargs["controller"] = MagicMock
#         super().__init__(**kwargs)


def main(password, controller):
    import ssl

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    component = Component(
        transports=[
            {
                "type": "websocket",
                "url": "wss://wamp.2e0byo.co.uk:3227/ws",
                "endpoint": {
                    "type": "tcp",
                    "host": "wamp.2e0byo.co.uk",
                    "port": 3227,
                    "tls": context,
                },
            },
        ],
        realm="miniature-lighting-controller",
        authentication={
            "ticket": {
                "authid": "public",
                "ticket": password,
            },
        },
    )
    server = Backend(controller=controller, component=component)

    print("\n Starting Backend\n Press Ctrl-c to exit\n")
    server.run()

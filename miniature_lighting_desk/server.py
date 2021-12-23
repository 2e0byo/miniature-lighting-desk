import asyncio
import contextlib
import socket
import socketserver
import threading
import time
from logging import getLogger

import uvicorn
from fastapi import FastAPI
from fastapi_websocket_rpc import RpcMethodsBase, WebsocketRPCEndpoint
from fastapi_websocket_pubsub import PubSubEndpoint

from . import async_hal as hal


class ControllerServer(RpcMethodsBase):
    """Server controlling a miniature lighting controller."""

    instances = []

    def __init__(self, channels: int = 8, channel=None, controller=None):
        self.name = f"ControllerServer-{len(self.instances)}"
        self.instances.append(self.name)
        self._logger = getLogger(self.name)

        self.controller = controller() if controller else hal.Controller()
        channel = channel or hal.Channel
        self.channels = [channel(self.controller, i) for i in range(channels)]
        self.vals = []
        self._pubsub_endpoint: PubSubEndpoint = None
        self.sync()

    async def ping(self):
        return "hello"

    async def set_brightness(self, *, channel: int, val: int):
        if self.vals[channel] != val:
            self._logger.debug(f"Setting channel {channel} to val {val}")
            self.channels[channel].set_brightness(val)
            self.vals[channel] = val
            if self._pubsub_endpoint:
                self._pubsub_endpoint.publish(
                    dict(zip(range(len(self.channels)), self.channels))
                )

    async def get_brightness(self, *, channel: int):
        self._logger.debug(f"Got {self.vals[channel]} for channel {channel}")
        return self.vals[channel]

    def sync(self):
        self.vals = [channel.get_brightness() for channel in self.channels]


class SocketServer(uvicorn.Server):
    """Socket Server exposing a controller."""

    instances = []
    DEFAULT_PORT = 3227
    DEFAULT_ENDPOINT = "/ws"
    DEFAULT_PUBSUB_ENDPOINT = "/pubsub"

    def __init__(
        self,
        *args,
        controller_server: ControllerServer,
        endpoint: str = None,
        pubsub_endpoint: str = None,
        **kwargs,
    ):
        self.name = f"SocketServer-{len(self.instances)}"
        self.instances.append(self.name)
        self._logger = getLogger(self.name)
        self._ip = None
        self._port = None
        self._app = FastAPI()
        self._controller = controller_server
        self.endpoint = endpoint or self.DEFAULT_ENDPOINT
        self._endpoint = WebsocketRPCEndpoint(self._controller)
        self._endpoint.register_route(self._app, self.endpoint)
        self._pubsub_endpoint = pubsub_endpoint or self.DEFAULT_PUBSUB_ENDPOINT
        self.controller._pubsub_endpoint = self._pubsub_endpoint
        config = uvicorn.Config(self._app, port=self.port, host="0.0.0.0")
        super().__init__(*args, **kwargs, config=config)

    @property
    def ip(self):
        if not self._ip:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.connect(("8.8.8.8", 80))
                self._ip = sock.getsockname()[0]
        return self._ip

    @property
    def port(self) -> int:
        if not self._port:
            try:
                with socketserver.TCPServer(
                    ("localhost", self.DEFAULT_PORT), None
                ) as s:
                    self._port = s.server_address[1]
            except Exception as e:
                self._logger.exception(e)
                with socketserver.TCPServer(("localhost", 0), None) as s:
                    self._port = s.server_address[1]

        return self._port

    def install_signal_handlers(self):
        """Prevent signal handlers from being installed."""

    @contextlib.contextmanager
    def run_in_thread(self):
        port = self.port
        ip = self.ip
        self._logger.info(f"Starting server at {ip} on port {port}")
        thread = threading.Thread(target=self.run)
        thread.start()
        try:
            while not self.started:
                time.sleep(1e-3)
            yield self._controller
        finally:
            self.should_exit = True
            thread.join()


def Server():
    """Standard server."""
    return SocketServer(controller_server=ControllerServer())

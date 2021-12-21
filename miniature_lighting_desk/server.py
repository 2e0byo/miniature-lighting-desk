from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
from multiprocessing import Process
import socketserver
import socket
from logging import getLogger
import logging

from . import async_hal as hal


class Server:
    """Server controlling a miniature lighting controller."""

    DEFAULT_PORT = 3227
    instances = []

    def __init__(self, channels: int = 8):
        self.name = f"Server-{len(self.instances)}"
        self.instances.append(self.name)
        self._logger = getLogger(self.name)

        self.controller = hal.Controller()
        self.channels = [hal.Channel(self.controller, i) for i in range(channels)]
        self.vals = []
        self.sync()
        self._port = None
        self._ip = None
        self.server_thread = None
        server = SimpleJSONRPCServer(("localhost", self.port))
        server.register_function(self.set)
        server.register_function(self.get)
        server.register_function(self.sync)
        self.server = server

    def __enter__(self):
        self.server_thread = Process(target=self.server.serve_forever)
        proc = self.server_thread
        assert proc
        self.server_thread.start()
        self._logger.info(f"Started server at {self.ip} on port {self.port}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        proc = self.server_thread
        proc.terminate()
        proc.join(2)
        if proc.is_alive():
            self._logger.info("Server failed to die; killing...")
            proc.kill()
            proc.join(2)
            if proc.is_alive():
                raise Exception("Failed to kill server thread.")
        self._logger.info("Server died.")

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
                with socketserver.TCPServer(("localhost", 0), None) as s:
                    self._port = s.server_address[1]

        return self._port

    def set(self, channel: int, val: int):
        if self.vals[channel] != val:
            self.channels[channel].set_brightness(val)
        self.vals[channel] = val

    def get(self, channel: int):
        return self.vals[channel]

    def sync(self):
        self.vals = [channel.get_brightness() for channel in self.channels]

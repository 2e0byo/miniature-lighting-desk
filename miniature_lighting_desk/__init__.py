from unittest.mock import patch

import coloredlogs

from .server import Server

coloredlogs.install()


class MockChannel:
    def __init__(self):
        self.val = 0

    def get_brightness(self):
        return self.val

    def set_brightness(self, val):
        self.val = max(0, min(255, val))


@patch(f"{__name__}.server.hal.Controller")
def MockServer(*args):
    """A mock server for testing."""
    s = Server()
    s.channels = [MockChannel()] * 8
    s.sync()
    return s


def test_server():
    s = MockServer()
    s.__enter__()

import pytest
from miniature_lighting_desk import server


class MockChannel:
    def __init__(self):
        self.val = 0

    def get_brightness(self):
        return self.val

    def set_brightness(self, val):
        self.val = val


@pytest.fixture
def Server(mocker):
    """Server with mocked hal"""
    controller = mocker.patch("miniature_lighting_desk.server.hal.Controller")
    s = server.Server()
    s.channels = [MockChannel()] * 8
    s.sync()
    with s:
        yield s


def test_init(Server):
    assert [Server.get(i) for i in range(8)] == [0] * 8


def test_set(Server):
    for i in range(8):
        assert Server.get(i) != 199
        Server.set(i, 199)
        assert Server.get(i) == 199

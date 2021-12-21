import pytest
from miniature_lighting_desk import server, MockServer
import jsonrpclib


class MockChannel:
    def __init__(self):
        self.val = 0

    def get_brightness(self):
        return self.val

    def set_brightness(self, val):
        self.val = val


@pytest.fixture
def Server():
    s = MockServer()
    with s:
        yield s


def test_init(Server):
    assert [Server.get(i) for i in range(8)] == [0] * 8


def test_set(Server):
    for i in range(8):
        assert Server.get(i) != 199
        Server.set(i, 199)
        assert Server.get(i) == 199


def test_jsonrpc(Server):
    s = jsonrpclib.Server(f"http://localhost:{Server.port}")
    s.sync()
    assert s.get(0) == 0
    s.set(1, 20)
    assert s.get(1) == 20
    with pytest.raises(jsonrpclib.jsonrpc.ProtocolError):
        s.nosuchmethod(22)

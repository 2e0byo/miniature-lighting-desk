import asyncio
from functools import partial

import pytest
from fastapi_websocket_rpc import RpcMethodsBase, WebSocketRpcClient
from miniature_lighting_desk.test_server import MockServer


async def run_client(uri, method, **kwargs):
    async with WebSocketRpcClient(uri, RpcMethodsBase()) as client:
        res = await getattr(client.other, method)(**kwargs)
        try:
            return int(res.result)
        except ValueError:
            return res.result


@pytest.fixture
def Server():
    s = MockServer()
    with s.run_in_thread() as cont:
        yield cont, partial(run_client, f"ws://localhost:{s.port}{s.endpoint}")


@pytest.mark.asyncio
async def test_init(Server):
    server, run_method = Server
    assert [await server.get_brightness(channel=i) for i in range(8)] == [0] * 8


@pytest.mark.asyncio
async def test_set(Server):
    server, run_method = Server
    for i in range(8):
        assert await server.get_brightness(channel=i) != 199
        await server.set_brightness(channel=i, val=199)
        assert await server.get_brightness(channel=i) == 199


@pytest.mark.asyncio
async def test_ping(Server):
    server, run_method = Server
    assert await run_method("ping") == "hello"


@pytest.mark.asyncio
async def test_rpc(Server):
    server, run_method = Server
    for i in range(8):
        assert await run_method("get_brightness", channel=i) != 199
        await run_method("set_brightness", channel=i, val=199)
        assert await run_method("get_brightness", channel=i) == 199

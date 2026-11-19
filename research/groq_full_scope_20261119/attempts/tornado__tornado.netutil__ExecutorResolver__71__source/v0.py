import asyncio
import concurrent.futures
import socket
import pytest
from tornado.netutil import ExecutorResolver

@pytest.mark.asyncio
async def test_resolve_success():
    resolver = ExecutorResolver()
    resolver.initialize()
    # Resolve a known host; should return at least one address
    result = await resolver.resolve("localhost", 80)
    assert isinstance(result, list)
    assert len(result) > 0
    # Each entry is a tuple (family, sockaddr)
    for family, sockaddr in result:
        assert isinstance(family, int)
        assert isinstance(sockaddr, tuple)
    resolver.close()

@pytest.mark.asyncio
async def test_resolve_invalid_host():
    resolver = ExecutorResolver()
    resolver.initialize()
    with pytest.raises(socket.gaierror):
        await resolver.resolve("nonexistent.host.example", 80)
    resolver.close()

def test_close_shuts_executor():
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    resolver = ExecutorResolver()
    resolver.initialize(executor=executor, close_executor=True)
    # Ensure executor is alive
    assert not executor._shutdown
    resolver.close()
    # After close, executor should be shutdown
    assert executor._shutdown
    # Subsequent calls should raise RuntimeError because executor is None
    with pytest.raises(RuntimeError):
        asyncio.run(resolver.resolve("localhost", 80))

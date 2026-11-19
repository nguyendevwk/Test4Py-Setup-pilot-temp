import asyncio
import concurrent.futures
import socket
import pytest
from tornado.netutil import ExecutorResolver

# Helper to run the async resolve in the event loop
async def async_resolve(resolver, host, port, family=socket.AF_UNSPEC):
    return await resolver.resolve(host, port, family)

@pytest.mark.asyncio
async def test_resolve_success():
    """ExecutorResolver should resolve a known host to at least one address."""
    resolver = ExecutorResolver()
    resolver.initialize()
    # Resolve localhost; should return at least one IPv4 or IPv6 address
    results = await async_resolve(resolver, "localhost", 80)
    assert isinstance(results, list)
    assert len(results) >= 1
    for family, addr in results:
        assert family in (socket.AF_INET, socket.AF_INET6)
        assert isinstance(addr, tuple)
    resolver.close()

@pytest.mark.asyncio
async def test_resolve_invalid_host_raises():
    """Resolving an invalid hostname should raise a socket.gaierror."""
    resolver = ExecutorResolver()
    resolver.initialize()
    with pytest.raises(socket.gaierror):
        await async_resolve(resolver, "nonexistent.host.example", 80)
    resolver.close()

def test_executor_shutdown_on_close():
    """Closing the resolver should shut down the executor if close_executor=True."""
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    resolver = ExecutorResolver()
    resolver.initialize(executor=executor, close_executor=True)
    # Submit a dummy task to ensure executor is active
    future = executor.submit(lambda: 42)
    assert future.result() == 42
    # Close resolver and check executor is shut down
    resolver.close()
    assert executor._shutdown is True
    # Subsequent submit should raise RuntimeError
    with pytest.raises(RuntimeError):
        executor.submit(lambda: 1)

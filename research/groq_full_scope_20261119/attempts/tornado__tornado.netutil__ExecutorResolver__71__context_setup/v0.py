import asyncio
import concurrent.futures
import socket
import pytest
from tornado.netutil import ExecutorResolver, _resolve_addr


@pytest.mark.asyncio
async def test_executor_resolver_resolves_localhost(tmp_path):
    """ExecutorResolver should resolve a valid hostname to a list of (family, address)."""
    resolver = ExecutorResolver()
    resolver.initialize(concurrent.futures.ThreadPoolExecutor(max_workers=2))
    # Resolve localhost on an arbitrary port (80 is common)
    result = await resolver.resolve("localhost", 80)
    # Each entry should be a tuple of (family, address)
    assert isinstance(result, list)
    assert all(isinstance(item, tuple) and len(item) == 2 for item in result)
    families, addresses = zip(*result)
    # All families should be either AF_INET or AF_INET6
    assert all(f in (socket.AF_INET, socket.AF_INET6) for f in families)
    # Addresses should be tuples suitable for socket.connect
    assert all(isinstance(addr, tuple) for addr in addresses)
    resolver.close()
    # After close, executor should be None
    assert resolver.executor is None


def test_executor_resolver_shuts_down_executor():
    """Closing the resolver should shut down the executor if close_executor is True."""
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    resolver = ExecutorResolver()
    resolver.initialize(executor=executor, close_executor=True)
    # Ensure executor is running
    assert not executor._shutdown
    resolver.close()
    # After close, executor should be shut down
    assert executor._shutdown


@pytest.mark.asyncio
async def test_executor_resolver_invalid_host_raises_ioerror():
    """Resolving an invalid hostname should raise an IOError."""
    resolver = ExecutorResolver()
    resolver.initialize(concurrent.futures.ThreadPoolExecutor(max_workers=1))
    with pytest.raises(IOError):
        await resolver.resolve("nonexistent.host.example", 80)
    resolver.close()

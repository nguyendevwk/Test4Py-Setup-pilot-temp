import asyncio
import concurrent.futures
import socket
import pytest
from tornado.netutil import ExecutorResolver, _resolve_addr


@pytest.mark.asyncio
async def test_executor_resolver_resolves_localhost():
    """ExecutorResolver should resolve 'localhost' to an IPv4 address."""
    resolver = ExecutorResolver()
    resolver.initialize(concurrent.futures.ThreadPoolExecutor(max_workers=1))
    # Resolve using the executor (runs in a thread)
    result = await resolver.resolve("localhost", 80)
    # There should be at least one IPv4 address
    ipv4_addresses = [addr for fam, addr in result if fam == socket.AF_INET]
    assert ipv4_addresses, "No IPv4 address found for localhost"
    # The returned address should be a tuple (host, port)
    host, port = ipv4_addresses[0]
    assert host in ("127.0.0.1", "localhost")
    assert port == 80
    resolver.close()
    # After close, the executor should be shutdown
    assert resolver.executor is None


def test_executor_resolver_invalid_host_raises_ioerror():
    """Resolving an invalid hostname should raise IOError."""
    resolver = ExecutorResolver()
    resolver.initialize(concurrent.futures.ThreadPoolExecutor(max_workers=1))
    with pytest.raises(IOError):
        asyncio.get_event_loop().run_until_complete(
            resolver.resolve("nonexistent.host.example", 80)
        )
    resolver.close()


@pytest.mark.asyncio
async def test_executor_resolver_dummy_executor():
    """When no executor is supplied, dummy_executor is used and not shut down."""
    resolver = ExecutorResolver()
    resolver.initialize()  # uses dummy_executor
    result = await resolver.resolve("localhost", 80)
    # dummy_executor runs in the current thread, so result should be immediate
    assert isinstance(result, list)
    resolver.close()
    # dummy_executor should not be shutdown, executor attribute set to None
    assert resolver.executor is None

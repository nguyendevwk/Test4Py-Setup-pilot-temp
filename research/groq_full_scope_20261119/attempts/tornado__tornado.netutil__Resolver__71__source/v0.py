import asyncio
import socket
import pytest
from tornado.netutil import DefaultLoopResolver, Resolver

@pytest.mark.asyncio
async def test_resolver_success():
    resolver: Resolver = DefaultLoopResolver()
    # Resolve a known hostname (localhost) on a common port
    results = await resolver.resolve("localhost", 80)
    # Expect at least one IPv4 or IPv6 address
    assert isinstance(results, list) and len(results) > 0
    for family, addr in results:
        # addr should be a tuple suitable for socket.connect
        assert isinstance(addr, tuple)
        # The port in the tuple should match the requested port
        assert addr[-1] == 80
        # family should be a valid AddressFamily
        assert family in (socket.AF_INET, socket.AF_INET6)

@pytest.mark.asyncio
async def test_resolver_invalid_host():
    resolver: Resolver = DefaultLoopResolver()
    with pytest.raises(IOError):
        await resolver.resolve("nonexistent.host.example", 80)

@pytest.mark.asyncio
async def test_resolver_boundary_port():
    resolver: Resolver = DefaultLoopResolver()
    # Use the lowest valid port number (0 is allowed for bind, but not for connect)
    # Here we test that resolving port 0 does not raise an error and returns a result
    results = await resolver.resolve("localhost", 0)
    assert isinstance(results, list) and len(results) > 0
    for family, addr in results:
        assert addr[-1] == 0

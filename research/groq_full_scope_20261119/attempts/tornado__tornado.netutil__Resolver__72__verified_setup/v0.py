import asyncio
import socket
import pytest
from tornado.netutil import Resolver, DefaultLoopResolver

# Test 1: Normal resolution of a known hostname
@pytest.mark.asyncio
async def test_resolve_localhost_success():
    resolver = DefaultLoopResolver()
    result = await resolver.resolve("localhost", 80)
    # Expect at least one IPv4 or IPv6 address
    assert isinstance(result, list) and len(result) > 0
    for family, addr in result:
        assert family in (socket.AF_INET, socket.AF_INET6)
        # addr should be a tuple (host, port) or (host, port, flowinfo, scopeid)
        assert isinstance(addr, tuple)
        assert addr[1] == 80
    resolver.close()

# Test 2: Resolve with explicit IPv4 family
@pytest.mark.asyncio
async def test_resolve_ipv4_family():
    resolver = DefaultLoopResolver()
    result = await resolver.resolve("localhost", 80, family=socket.AF_INET)
    # All returned families should be AF_INET
    assert all(family == socket.AF_INET for family, _ in result)
    resolver.close()

# Test 3: Resolve an invalid hostname should raise IOError
@pytest.mark.asyncio
async def test_resolve_invalid_host_error():
    resolver = DefaultLoopResolver()
    with pytest.raises(IOError):
        await resolver.resolve("nonexistent.invalid.host", 80)
    resolver.close()

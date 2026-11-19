import asyncio
import socket
import pytest
from tornado.netutil import Resolver, DefaultLoopResolver

# Test 1: Normal resolution of a known hostname
@pytest.mark.asyncio
async def test_resolve_localhost():
    resolver = DefaultLoopResolver()
    results = await resolver.resolve("localhost", 80)
    assert isinstance(results, list) and len(results) > 0
    # Each result is a tuple (family, address)
    for family, address in results:
        assert isinstance(family, int)
        # address should be a tuple suitable for socket.connect
        assert isinstance(address, tuple)
        # For IPv4, address[0] should be an IP string
        if family == socket.AF_INET:
            assert isinstance(address[0], str)
            assert isinstance(address[1], int)
        # For IPv6, address[0] should be an IP string
        if family == socket.AF_INET6:
            assert isinstance(address[0], str)
            assert isinstance(address[1], int)

# Test 2: Boundary case – resolving an invalid hostname should raise IOError
@pytest.mark.asyncio
async def test_resolve_invalid_hostname():
    resolver = DefaultLoopResolver()
    with pytest.raises(IOError):
        await resolver.resolve("nonexistent.host.example", 80)

# Test 3: Error case – passing a non-string host should raise TypeError
@pytest.mark.asyncio
async def test_resolve_nonstring_host():
    resolver = DefaultLoopResolver()
    with pytest.raises(TypeError):
        await resolver.resolve(12345, 80)

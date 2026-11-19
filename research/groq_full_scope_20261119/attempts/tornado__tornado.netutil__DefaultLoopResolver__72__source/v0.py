import asyncio
import socket
import pytest
from tornado.netutil import DefaultLoopResolver

@pytest.mark.asyncio
async def test_resolve_localhost_returns_addresses():
    resolver = DefaultLoopResolver()
    # Resolve a common host that should exist on any system
    results = await resolver.resolve("localhost", 80)
    # Each result is a tuple (family, address)
    assert isinstance(results, list)
    assert len(results) > 0
    for fam, addr in results:
        assert fam in (socket.AF_INET, socket.AF_INET6)
        # Address should be a tuple of (host, port)
        assert isinstance(addr, tuple)
        assert addr[1] == 80

@pytest.mark.asyncio
async def test_resolve_with_specific_family():
    resolver = DefaultLoopResolver()
    # Force IPv4 resolution
    results = await resolver.resolve("localhost", 80, family=socket.AF_INET)
    assert all(fam == socket.AF_INET for fam, _ in results)

@pytest.mark.asyncio
async def test_resolve_invalid_host_raises_gaierror():
    resolver = DefaultLoopResolver()
    with pytest.raises(socket.gaierror):
        await resolver.resolve("this-host-should-not-exist.example", 80)

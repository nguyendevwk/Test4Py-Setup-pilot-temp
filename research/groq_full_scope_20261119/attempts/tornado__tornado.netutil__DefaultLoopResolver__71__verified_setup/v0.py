import asyncio
import socket
import pytest
from tornado.netutil import DefaultLoopResolver


@pytest.mark.asyncio
async def test_resolve_localhost_ipv4():
    """Resolve localhost on port 80 and ensure IPv4 addresses are returned."""
    resolver = DefaultLoopResolver()
    results = await resolver.resolve("localhost", 80, family=socket.AF_INET)
    # All returned families should be AF_INET
    assert all(fam == socket.AF_INET for fam, _ in results)
    # Each address should be a tuple of (host, port)
    assert all(isinstance(addr, tuple) and len(addr) == 2 for _, addr in results)
    # The port in the address should match the requested port
    assert all(addr[1] == 80 for _, addr in results)


@pytest.mark.asyncio
async def test_resolve_invalid_host_raises():
    """Resolving an invalid hostname should raise an OSError."""
    resolver = DefaultLoopResolver()
    with pytest.raises(OSError):
        await resolver.resolve("nonexistent.host.example", 80)


@pytest.mark.asyncio
async def test_resolve_port_zero_returns_wildcard():
    """Resolving with port 0 should return addresses with port 0 (wildcard)."""
    resolver = DefaultLoopResolver()
    results = await resolver.resolve("localhost", 0, family=socket.AF_UNSPEC)
    # At least one result should be returned
    assert len(results) > 0
    # Each address should have port 0
    assert all(addr[1] == 0 for _, addr in results)

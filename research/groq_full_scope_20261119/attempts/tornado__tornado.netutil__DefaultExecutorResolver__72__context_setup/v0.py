import asyncio
import socket
import pytest
from tornado.netutil import DefaultExecutorResolver


@pytest.mark.asyncio
async def test_resolve_valid_host():
    resolver = DefaultExecutorResolver()
    # Resolve a well‑known host; expect at least one IPv4 or IPv6 address
    results = await resolver.resolve("localhost", 80)
    assert isinstance(results, list)
    assert len(results) >= 1
    for fam, addr in results:
        assert fam in (socket.AF_INET, socket.AF_INET6)
        # addr should be a tuple (host, port) or (host, port, flowinfo, scopeid)
        assert isinstance(addr, tuple)
        assert addr[1] == 80


@pytest.mark.asyncio
async def test_resolve_invalid_host_raises():
    resolver = DefaultExecutorResolver()
    with pytest.raises(OSError):
        await resolver.resolve("nonexistent.host.example", 80)


@pytest.mark.asyncio
async def test_resolve_port_boundary():
    resolver = DefaultExecutorResolver()
    # Port 0 is reserved; getaddrinfo should still return an address with port 0
    results = await resolver.resolve("localhost", 0)
    assert isinstance(results, list)
    assert len(results) >= 1
    for fam, addr in results:
        assert fam in (socket.AF_INET, socket.AF_INET6)
        assert addr[1] == 0

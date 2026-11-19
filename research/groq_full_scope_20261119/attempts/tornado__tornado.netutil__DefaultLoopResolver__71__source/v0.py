import asyncio
import socket
import pytest
from tornado.netutil import DefaultLoopResolver

@pytest.mark.asyncio
async def test_resolve_localhost_returns_ipv4_and_ipv6():
    resolver = DefaultLoopResolver()
    results = await resolver.resolve("localhost", 80)
    families = {fam for fam, _ in results}
    # Expect both IPv4 and IPv6 families if available
    assert socket.AF_INET in families
    assert socket.AF_INET6 in families
    # Each address should be a tuple of (host, port)
    for _, addr in results:
        host, port = addr
        assert isinstance(host, str)
        assert port == 80

@pytest.mark.asyncio
async def test_resolve_invalid_host_raises():
    resolver = DefaultLoopResolver()
    with pytest.raises(socket.gaierror):
        await resolver.resolve("nonexistent.host.example", 80)

@pytest.mark.asyncio
async def test_resolve_invalid_port_raises():
    resolver = DefaultLoopResolver()
    # Port numbers must be in 0-65535; 70000 is invalid
    with pytest.raises(ValueError):
        await resolver.resolve("localhost", 70000)

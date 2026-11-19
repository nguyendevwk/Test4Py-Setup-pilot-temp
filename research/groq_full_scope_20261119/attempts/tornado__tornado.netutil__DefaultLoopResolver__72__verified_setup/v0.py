import asyncio
import socket
import pytest
from tornado.netutil import DefaultLoopResolver


@pytest.mark.asyncio
async def test_resolve_localhost_returns_addresses():
    resolver = DefaultLoopResolver()
    # Resolve a common service port that should exist on localhost
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
async def test_resolve_invalid_host_raises_gaierror():
    resolver = DefaultLoopResolver()
    with pytest.raises(socket.gaierror):
        await resolver.resolve("this.host.does.not.exist", 80)


@pytest.mark.asyncio
async def test_resolve_with_specific_family():
    resolver = DefaultLoopResolver()
    # Resolve using IPv4 family only
    results = await resolver.resolve("localhost", 80, family=socket.AF_INET)
    assert all(fam == socket.AF_INET for fam, _ in results)
    # Resolve using IPv6 family only
    results6 = await resolver.resolve("localhost", 80, family=socket.AF_INET6)
    # Depending on the system, IPv6 may or may not be available; if not, the list may be empty
    if results6:
        assert all(fam == socket.AF_INET6 for fam, _ in results6)

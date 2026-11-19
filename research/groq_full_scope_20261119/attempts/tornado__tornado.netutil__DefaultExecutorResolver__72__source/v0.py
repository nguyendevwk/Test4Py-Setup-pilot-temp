import asyncio
import socket
import pytest
from tornado.netutil import DefaultExecutorResolver

@pytest.mark.asyncio
async def test_resolve_localhost_returns_addresses():
    resolver = DefaultExecutorResolver()
    result = await resolver.resolve("localhost", 80)
    # Expect at least one address tuple (family, type, proto, canonname, sockaddr)
    assert isinstance(result, list)
    assert len(result) > 0
    for addr in result:
        assert isinstance(addr, tuple)
        assert len(addr) == 5
        family, _, _, _, sockaddr = addr
        assert isinstance(family, int)
        assert isinstance(sockaddr, tuple)
        # sockaddr should contain host and port
        assert isinstance(sockaddr[0], str)
        assert isinstance(sockaddr[1], int)

@pytest.mark.asyncio
async def test_resolve_invalid_host_raises_gaierror():
    resolver = DefaultExecutorResolver()
    with pytest.raises(socket.gaierror):
        await resolver.resolve("nonexistent.invalid", 80)

@pytest.mark.asyncio
async def test_resolve_port_zero_returns_addresses_with_zero_port():
    resolver = DefaultExecutorResolver()
    result = await resolver.resolve("localhost", 0)
    assert isinstance(result, list)
    assert len(result) > 0
    for addr in result:
        _, _, _, _, sockaddr = addr
        # The port part of the sockaddr should be 0
        assert sockaddr[1] == 0

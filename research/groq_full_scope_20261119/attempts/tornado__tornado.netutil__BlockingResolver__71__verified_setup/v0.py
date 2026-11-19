import asyncio
import socket
import pytest
from tornado.netutil import BlockingResolver

@pytest.mark.asyncio
async def test_resolve_localhost_returns_address_info():
    resolver = BlockingResolver()
    # Resolve a known host and port; should return at least one address tuple
    result = await resolver.resolve('localhost', 80)
    assert isinstance(result, list)
    assert len(result) > 0
    # Each entry should be a tuple of (family, type, proto, canonname, sockaddr)
    for entry in result:
        assert isinstance(entry, tuple)
        assert len(entry) == 5
        family, socktype, proto, canonname, sockaddr = entry
        assert isinstance(family, int)
        assert isinstance(socktype, int)
        assert isinstance(proto, int)
        assert isinstance(canonname, str)
        assert isinstance(sockaddr, tuple)
        # For IPv4, sockaddr should be (address, port)
        if family == socket.AF_INET:
            assert isinstance(sockaddr[0], str)
            assert isinstance(sockaddr[1], int)

@pytest.mark.asyncio
async def test_resolve_invalid_host_raises_gaierror():
    resolver = BlockingResolver()
    with pytest.raises(socket.gaierror):
        await resolver.resolve('this.host.does.not.exist', 80)

@pytest.mark.asyncio
async def test_resolve_with_invalid_port_raises_valueerror():
    resolver = BlockingResolver()
    # Passing a non-integer port should raise a ValueError before calling getaddrinfo
    with pytest.raises(ValueError):
        await resolver.resolve('localhost', 'not-a-port')

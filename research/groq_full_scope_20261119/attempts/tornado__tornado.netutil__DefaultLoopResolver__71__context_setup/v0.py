import asyncio
import socket
import pytest
from tornado.netutil import DefaultLoopResolver


@pytest.mark.asyncio
async def test_resolve_localhost_returns_ipv4_and_ipv6():
    resolver = DefaultLoopResolver()
    results = await resolver.resolve("localhost", 80)
    families = {fam for fam, _ in results}
    # Expect at least one IPv4 and one IPv6 address
    assert socket.AF_INET in families
    assert socket.AF_INET6 in families
    # Each address tuple should contain the port we requested
    for _, addr in results:
        assert addr[1] == 80


@pytest.mark.asyncio
async def test_resolve_invalid_host_raises_ioerror():
    resolver = DefaultLoopResolver()
    with pytest.raises(IOError):
        await resolver.resolve("nonexistent.host.example", 80)


@pytest.mark.asyncio
async def test_resolve_with_family_specification():
    resolver = DefaultLoopResolver()
    # Resolve only IPv4 addresses
    results_ipv4 = await resolver.resolve("localhost", 80, family=socket.AF_INET)
    assert all(fam == socket.AF_INET for fam, _ in results_ipv4)
    # Resolve only IPv6 addresses
    results_ipv6 = await resolver.resolve("localhost", 80, family=socket.AF_INET6)
    assert all(fam == socket.AF_INET6 for fam, _ in results_ipv6)

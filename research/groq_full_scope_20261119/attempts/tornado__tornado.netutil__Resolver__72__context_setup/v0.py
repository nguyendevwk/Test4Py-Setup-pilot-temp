import asyncio
import socket
import pytest
from tornado.netutil import DefaultLoopResolver, Resolver


@pytest.mark.asyncio
async def test_resolver_success():
    """Resolver should return a non‑empty list of address tuples for a known host."""
    resolver = DefaultLoopResolver()
    results = await resolver.resolve("localhost", 80)
    # Each result is a tuple (family, address)
    assert isinstance(results, list) and len(results) > 0
    for fam, addr in results:
        assert fam in (socket.AF_INET, socket.AF_INET6)
        # addr should be a tuple suitable for socket.connect
        assert isinstance(addr, tuple)
        # For IPv4, addr[0] is the IP string, addr[1] is the port
        if fam == socket.AF_INET:
            assert isinstance(addr[0], str)
            assert addr[1] == 80
        # For IPv6, addr[0] is the IP string, addr[1] is the port
        if fam == socket.AF_INET6:
            assert isinstance(addr[0], str)
            assert addr[1] == 80


@pytest.mark.asyncio
async def test_resolver_invalid_host():
    """Resolver should raise an IOError when the host cannot be resolved."""
    resolver = DefaultLoopResolver()
    with pytest.raises(IOError):
        await resolver.resolve("nonexistent.host.example", 80)


@pytest.mark.asyncio
async def test_resolver_family_filter():
    """Resolver should respect the family argument and return only matching families."""
    resolver = DefaultLoopResolver()
    # Resolve with IPv4 only
    ipv4_results = await resolver.resolve("localhost", 80, family=socket.AF_INET)
    assert all(fam == socket.AF_INET for fam, _ in ipv4_results)

    # Resolve with IPv6 only
    ipv6_results = await resolver.resolve("localhost", 80, family=socket.AF_INET6)
    assert all(fam == socket.AF_INET6 for fam, _ in ipv6_results)

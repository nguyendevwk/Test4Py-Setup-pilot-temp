import asyncio
import socket
import pytest
from tornado.netutil import DefaultLoopResolver


@pytest.mark.asyncio
async def test_resolve_valid_host():
    resolver = DefaultLoopResolver()
    # Resolve a well‑known host; expect at least one IPv4 or IPv6 address
    results = await resolver.resolve("localhost", 80)
    assert isinstance(results, list)
    assert len(results) > 0
    for fam, addr in results:
        assert fam in (socket.AF_INET, socket.AF_INET6)
        # addr should be a tuple suitable for socket.connect
        assert isinstance(addr, tuple)
        assert addr[1] == 80  # port matches


@pytest.mark.asyncio
async def test_resolve_ipv6_only():
    resolver = DefaultLoopResolver()
    # Resolve a host that is expected to have IPv6 addresses only
    # Using the loopback IPv6 address ensures this
    results = await resolver.resolve("::1", 80, family=socket.AF_INET6)
    assert isinstance(results, list)
    assert len(results) > 0
    for fam, addr in results:
        assert fam == socket.AF_INET6
        assert addr[0] == "::1"
        assert addr[1] == 80


@pytest.mark.asyncio
async def test_resolve_invalid_host_raises():
    resolver = DefaultLoopResolver()
    with pytest.raises(OSError):
        await resolver.resolve("nonexistent.host.example", 80)

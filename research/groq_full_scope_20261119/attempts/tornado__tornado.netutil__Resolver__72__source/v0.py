import asyncio
import socket
import pytest
from tornado.netutil import Resolver, DefaultLoopResolver

# Test 1: Normal resolution of a known hostname
@pytest.mark.asyncio
async def test_resolve_known_host():
    resolver = Resolver()
    # Resolve localhost on port 80 (common port)
    result = await resolver.resolve("localhost", 80)
    # Expect at least one IPv4 or IPv6 address
    assert isinstance(result, list) and len(result) > 0
    for family, addr in result:
        assert family in (socket.AF_INET, socket.AF_INET6)
        # addr should be a tuple with host and port
        assert isinstance(addr, tuple)
        assert addr[1] == 80

# Test 2: Error handling for an invalid hostname
@pytest.mark.asyncio
async def test_resolve_invalid_host():
    resolver = Resolver()
    with pytest.raises(IOError):
        await resolver.resolve("nonexistent.host.example", 80)

# Test 3: Boundary family selection (AF_INET6 only)
@pytest.mark.asyncio
async def test_resolve_family_ipv6_only():
    resolver = Resolver()
    # Resolve localhost with IPv6 family only
    result = await resolver.resolve("localhost", 80, family=socket.AF_INET6)
    # If IPv6 is available, we should get IPv6 addresses
    if result:
        for family, addr in result:
            assert family == socket.AF_INET6
            assert addr[1] == 80
    else:
        # If no IPv6 addresses are available, the resolver should return an empty list
        assert result == []

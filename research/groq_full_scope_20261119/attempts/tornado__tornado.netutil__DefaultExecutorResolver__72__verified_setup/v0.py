import socket
import pytest
from tornado.netutil import DefaultExecutorResolver
from tornado.ioloop import IOLoop

@pytest.mark.asyncio
async def test_resolve_localhost_returns_ipv4_and_ipv6():
    resolver = DefaultExecutorResolver()
    # Resolve localhost for port 80 (common HTTP port)
    results = await resolver.resolve("localhost", 80, family=socket.AF_UNSPEC)
    # Expect at least one IPv4 and one IPv6 address
    ipv4 = [addr for addr in results if addr[0] == socket.AF_INET]
    ipv6 = [addr for addr in results if addr[0] == socket.AF_INET6]
    assert ipv4, "No IPv4 address returned for localhost"
    assert ipv6, "No IPv6 address returned for localhost"
    # Each tuple should contain the family and a socket address
    for family, addr in results:
        assert family in (socket.AF_INET, socket.AF_INET6)
        assert isinstance(addr, tuple)

@pytest.mark.asyncio
async def test_resolve_invalid_host_raises_exception():
    resolver = DefaultExecutorResolver()
    with pytest.raises(Exception) as excinfo:
        await resolver.resolve("nonexistent.host.example", 80)
    # The underlying exception should be a socket.gaierror or similar
    assert isinstance(excinfo.value, Exception)

@pytest.mark.asyncio
async def test_resolve_with_specific_family_returns_only_that_family():
    resolver = DefaultExecutorResolver()
    # Resolve using only IPv4 family
    results_ipv4 = await resolver.resolve("localhost", 80, family=socket.AF_INET)
    assert all(family == socket.AF_INET for family, _ in results_ipv4)
    # Resolve using only IPv6 family
    results_ipv6 = await resolver.resolve("localhost", 80, family=socket.AF_INET6)
    assert all(family == socket.AF_INET6 for family, _ in results_ipv6)

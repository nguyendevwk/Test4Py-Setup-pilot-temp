import socket
import pytest
from tornado.netutil import DefaultExecutorResolver

# Test normal resolution of a known host
def test_resolve_localhost():
    resolver = DefaultExecutorResolver()
    result = pytest.run_until_complete(resolver.resolve("localhost", 80))
    # Expect at least one IPv4 address tuple
    assert isinstance(result, list)
    assert len(result) > 0
    for family, addr in result:
        assert isinstance(family, int)
        assert isinstance(addr, tuple)
        # IPv4 addresses are 4-tuple, IPv6 are 6-tuple
        if family == socket.AF_INET:
            assert len(addr) == 4
        elif family == socket.AF_INET6:
            assert len(addr) == 6

# Test that resolving an invalid hostname raises a socket.gaierror
def test_resolve_invalid_host():
    resolver = DefaultExecutorResolver()
    with pytest.raises(socket.gaierror):
        pytest.run_until_complete(resolver.resolve("nonexistent.invalid.host", 80))

# Test boundary case: IPv6 loopback address
def test_resolve_ipv6_loopback():
    resolver = DefaultExecutorResolver()
    result = pytest.run_until_complete(
        resolver.resolve("::1", 80, family=socket.AF_INET6)
    )
    assert isinstance(result, list)
    assert len(result) > 0
    for family, addr in result:
        assert family == socket.AF_INET6
        assert isinstance(addr, tuple)
        assert len(addr) == 6

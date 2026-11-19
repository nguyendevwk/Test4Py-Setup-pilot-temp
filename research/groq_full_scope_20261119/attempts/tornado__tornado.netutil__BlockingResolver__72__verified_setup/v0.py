import socket
import pytest
from tornado.netutil import BlockingResolver

# Test 1: ensure initialize does not raise an exception
def test_blocking_resolver_initialize_no_error():
    resolver = BlockingResolver()
    # initialize should call the parent and not raise
    resolver.initialize()
    # After initialization, the resolver should have an executor attribute
    assert hasattr(resolver, "executor")

# Test 2: resolving an invalid hostname should raise a socket.gaierror
def test_blocking_resolver_resolve_invalid_host():
    resolver = BlockingResolver()
    resolver.initialize()
    with pytest.raises(socket.gaierror):
        resolver.resolve("nonexistent.host.example", 80)

# Test 3: resolving a known hostname returns a non-empty list of address info
def test_blocking_resolver_resolve_valid_host(tmp_path):
    resolver = BlockingResolver()
    resolver.initialize()
    # Use a hostname that is guaranteed to resolve (e.g., localhost)
    results = resolver.resolve("localhost", 80)
    assert isinstance(results, list)
    assert len(results) > 0
    # Each entry should be a tuple as returned by socket.getaddrinfo
    for entry in results:
        assert isinstance(entry, tuple)
        # The tuple should contain at least 5 elements
        assert len(entry) >= 5
        # The address part should be a tuple of (host, port)
        addr = entry[4]
        assert isinstance(addr, tuple)
        assert addr[1] == 80

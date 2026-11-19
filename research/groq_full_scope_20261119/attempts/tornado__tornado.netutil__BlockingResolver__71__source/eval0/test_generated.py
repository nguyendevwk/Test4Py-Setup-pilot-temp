import asyncio
import socket
import pytest
from tornado.netutil import BlockingResolver
from tornado.ioloop import IOLoop

# Test 1: verify that initialize calls the parent initialize method
def test_initialize_calls_super(monkeypatch):
    called = False

    def fake_super_initialize(self):
        nonlocal called
        called = True

    monkeypatch.setattr(
        BlockingResolver.__mro__[1],  # ExecutorResolver
        "initialize",
        fake_super_initialize,
        raising=True,
    )

    resolver = BlockingResolver()
    resolver.initialize()
    assert called, "BlockingResolver.initialize should call ExecutorResolver.initialize"

# Test 2: resolve a known hostname and verify that the returned addresses contain the expected IP
def test_resolve_known_hostname(tmp_path):
    resolver = BlockingResolver()
    # Use a hostname that is guaranteed to resolve (localhost)
    addresses = resolver.resolve("localhost", 80)
    # There should be at least one address
    assert len(addresses) > 0
    # All returned addresses should be tuples with at least 4 elements
    for addr in addresses:
        assert isinstance(addr, tuple)
        assert len(addr) >= 4
        # The IP part should be a string
        assert isinstance(addr[4][0], str)

# Test 3: resolve an invalid hostname and expect a socket.gaierror
def test_resolve_invalid_hostname():
    resolver = BlockingResolver()
    with pytest.raises(socket.gaierror):
        resolver.resolve("nonexistent.host.example", 80)

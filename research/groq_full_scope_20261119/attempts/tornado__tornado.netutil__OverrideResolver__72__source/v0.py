import asyncio
import socket
import pytest
from tornado.netutil import OverrideResolver, Resolver


class DummyResolver(Resolver):
    """A minimal resolver that records calls and returns a fixed result."""

    def __init__(self):
        self.calls = []

    async def resolve(self, host: str, port: int, family: socket.AddressFamily = socket.AF_UNSPEC):
        self.calls.append((host, port, family))
        # Return a single address tuple: (family, address, port, hostname)
        return [(family, f"{host}:{port}", port, host)]


@pytest.mark.asyncio
async def test_simple_override():
    """Test that a simple hostname override is applied."""
    dummy = DummyResolver()
    mapping = {"example.com": "127.0.0.1"}
    resolver = OverrideResolver()
    resolver.initialize(dummy, mapping)

    result = await resolver.resolve("example.com", 80)
    # The dummy resolver should have been called with the overridden host
    assert dummy.calls == [("127.0.0.1", 80, socket.AF_UNSPEC)]
    # The result should reflect the overridden host
    assert result == [(socket.AF_UNSPEC, "127.0.0.1:80", 80, "example.com")]


@pytest.mark.asyncio
async def test_host_port_override():
    """Test that a host+port override is applied correctly."""
    dummy = DummyResolver()
    mapping = {("login.example.com", 443): ("localhost", 1443)}
    resolver = OverrideResolver()
    resolver.initialize(dummy, mapping)

    result = await resolver.resolve("login.example.com", 443)
    # The dummy resolver should have been called with the overridden host and port
    assert dummy.calls == [("localhost", 1443, socket.AF_UNSPEC)]
    # The result should reflect the overridden host and port
    assert result == [(socket.AF_UNSPEC, "localhost:1443", 1443, "login.example.com")]


@pytest.mark.asyncio
async def test_host_port_family_override():
    """Test that a host+port+family override is applied correctly."""
    dummy = DummyResolver()
    mapping = {("login.example.com", 443, socket.AF_INET6): ("::1", 1443)}
    resolver = OverrideResolver()
    resolver.initialize(dummy, mapping)

    result = await resolver.resolve("login.example.com", 443, socket.AF_INET6)
    # The dummy resolver should have been called with the overridden host, port, and family
    assert dummy.calls == [( "::1", 1443, socket.AF_INET6)]
    # The result should reflect the overridden host, port, and family
    assert result == [(socket.AF_INET6, "::1:1443", 1443, "login.example.com")]

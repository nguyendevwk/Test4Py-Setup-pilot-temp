import asyncio
import socket
import pytest
from tornado.netutil import OverrideResolver

# A minimal resolver that records the arguments it was called with
class DummyResolver:
    def __init__(self):
        self.calls = []

    async def resolve(self, host, port, family=socket.AF_UNSPEC):
        self.calls.append((host, port, family))
        # Return a dummy address list
        return [(family, f"{host}:{port}")]

    def close(self):
        pass

@pytest.mark.asyncio
async def test_host_override():
    dummy = DummyResolver()
    resolver = OverrideResolver()
    resolver.initialize(dummy, {"example.com": "127.0.0.1"})
    result = await resolver.resolve("example.com", 80)
    assert dummy.calls == [("127.0.0.1", 80, socket.AF_UNSPEC)]
    assert result == [(socket.AF_UNSPEC, "127.0.0.1:80")]

@pytest.mark.asyncio
async def test_host_port_override():
    dummy = DummyResolver()
    resolver = OverrideResolver()
    resolver.initialize(dummy, {("example.com", 443): ("localhost", 8443)})
    result = await resolver.resolve("example.com", 443)
    assert dummy.calls == [("localhost", 8443, socket.AF_UNSPEC)]
    assert result == [(socket.AF_UNSPEC, "localhost:8443")]

@pytest.mark.asyncio
async def test_host_port_family_override():
    dummy = DummyResolver()
    resolver = OverrideResolver()
    resolver.initialize(dummy, {("example.com", 443, socket.AF_INET6): ("::1", 8443)})
    result = await resolver.resolve("example.com", 443, socket.AF_INET6)
    assert dummy.calls == [("::1", 8443, socket.AF_INET6)]
    assert result == [(socket.AF_INET6, "::1:8443")]

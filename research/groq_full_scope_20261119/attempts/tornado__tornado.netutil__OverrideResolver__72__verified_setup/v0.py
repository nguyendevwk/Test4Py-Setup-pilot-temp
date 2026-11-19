import asyncio
import socket
import pytest
from tornado.netutil import OverrideResolver, Resolver


class DummyResolver(Resolver):
    """A minimal resolver that returns a deterministic address list."""

    async def resolve(self, host: str, port: int, family: socket.AddressFamily = socket.AF_UNSPEC):
        # Return a single tuple with the family and a fake address string
        return [(family, f"{host}:{port}")]


@pytest.mark.asyncio
async def test_host_override(tmp_path):
    """Override a hostname to a different IP address."""
    resolver = DummyResolver()
    mapping = {"example.com": "127.0.1.1"}
    override = OverrideResolver()
    override.initialize(resolver, mapping)

    result = await override.resolve("example.com", 80)
    # The resolver should be called with the overridden host
    assert result == [(socket.AF_UNSPEC, "127.0.1.1:80")]


@pytest.mark.asyncio
async def test_host_port_override(tmp_path):
    """Override a hostname+port pair to a different host+port."""
    resolver = DummyResolver()
    mapping = {("login.example.com", 443): ("localhost", 1443)}
    override = OverrideResolver()
    override.initialize(resolver, mapping)

    result = await override.resolve("login.example.com", 443)
    # The resolver should be called with the overridden host and port
    assert result == [(socket.AF_UNSPEC, "localhost:1443")]


@pytest.mark.asyncio
async def test_host_port_family_override(tmp_path):
    """Override a hostname+port+family triplet to a different host+port."""
    resolver = DummyResolver()
    mapping = {("login.example.com", 443, socket.AF_INET6): ("::1", 1443)}
    override = OverrideResolver()
    override.initialize(resolver, mapping)

    result = await override.resolve("login.example.com", 443, socket.AF_INET6)
    # The resolver should be called with the overridden host and port, preserving the family
    assert result == [(socket.AF_INET6, "::1:1443")]

import asyncio
import socket
import pytest
from tornado.netutil import OverrideResolver, DefaultLoopResolver


@pytest.mark.asyncio
async def test_override_resolver_simple_host_override():
    """Test that a simple hostname override works."""
    resolver = DefaultLoopResolver()
    override = OverrideResolver()
    override.initialize(resolver, {"example.com": "127.0.0.1"})
    results = await override.resolve("example.com", 80)
    # All returned addresses should be for 127.0.0.1
    for fam, addr in results:
        assert addr[0] == "127.0.0.1"
        assert addr[1] == 80
    override.close()


@pytest.mark.asyncio
async def test_override_resolver_host_port_override():
    """Test that a host+port override works and preserves family."""
    resolver = DefaultLoopResolver()
    override = OverrideResolver()
    override.initialize(resolver, {("login.example.com", 443): ("localhost", 1443)})
    results = await override.resolve("login.example.com", 443, socket.AF_INET)
    # All returned addresses should be for localhost:1443
    for fam, addr in results:
        assert addr[0] in ("localhost", "127.0.0.1")
        assert addr[1] == 1443
    override.close()


@pytest.mark.asyncio
async def test_override_resolver_host_port_family_override():
    """Test that a host+port+family override works and returns IPv6."""
    resolver = DefaultLoopResolver()
    override = OverrideResolver()
    override.initialize(
        resolver,
        {("login.example.com", 443, socket.AF_INET6): ("::1", 1443)},
    )
    results = await override.resolve("login.example.com", 443, socket.AF_INET6)
    # All returned addresses should be IPv6 ::1:1443
    for fam, addr in results:
        assert fam == socket.AF_INET6
        assert addr[0] == "::1"
        assert addr[1] == 1443
    override.close()

import asyncio
import socket
import pytest
from tornado.netutil import OverrideResolver, DefaultLoopResolver


@pytest.mark.asyncio
async def test_host_override():
    """Override a hostname to a literal IP address."""
    resolver = OverrideResolver()
    resolver.initialize(DefaultLoopResolver(), {"example.com": "127.0.0.1"})
    # Resolve a known port on localhost; should return an IPv4 address
    results = await resolver.resolve("example.com", 80)
    assert all(fam == socket.AF_INET for fam, _ in results)
    # The resolved host should be 127.0.0.1
    assert any(addr[0] == "127.0.0.1" for _, addr in results)


@pytest.mark.asyncio
async def test_host_port_override():
    """Override a host+port pair to a different host+port."""
    resolver = OverrideResolver()
    resolver.initialize(
        DefaultLoopResolver(),
        {("login.example.com", 443): ("localhost", 1443)},
    )
    # Resolve the overridden pair; should connect to localhost:1443
    results = await resolver.resolve("login.example.com", 443)
    assert any(addr[1] == 1443 for _, addr in results)
    # The host part should be localhost
    assert any(addr[0] == "127.0.0.1" or addr[0] == "::1" for _, addr in results)


@pytest.mark.asyncio
async def test_host_port_family_override():
    """Override a host+port+family triplet to a different host+port."""
    resolver = OverrideResolver()
    resolver.initialize(
        DefaultLoopResolver(),
        {
            ("login.example.com", 443, socket.AF_INET6): ("::1", 1443),
        },
    )
    # Resolve with IPv6 family; should return an IPv6 address
    results = await resolver.resolve("login.example.com", 443, socket.AF_INET6)
    assert all(fam == socket.AF_INET6 for fam, _ in results)
    # The resolved host should be ::1 and port 1443
    assert any(addr[0] == "::1" and addr[1] == 1443 for _, addr in results)

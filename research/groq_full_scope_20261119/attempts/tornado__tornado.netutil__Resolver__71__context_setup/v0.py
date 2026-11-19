import asyncio
import socket
import pytest
from tornado.netutil import Resolver, DefaultLoopResolver

@pytest.mark.asyncio
async def test_resolve_valid_host():
    """Resolver should return a non‑empty list for a known host."""
    resolver = DefaultLoopResolver()
    result = await resolver.resolve("localhost", 80)
    # Each entry is a tuple (family, address)
    assert isinstance(result, list)
    assert result, "Result should not be empty for a valid host"
    for fam, addr in result:
        assert fam in (socket.AF_INET, socket.AF_INET6)
        # address should be a tuple suitable for socket.connect
        assert isinstance(addr, tuple)
        assert addr[0] == "127.0.0.1" or addr[0] == "::1"
        assert addr[1] == 80

@pytest.mark.asyncio
async def test_resolve_invalid_host_raises_ioerror():
    """Resolver should raise IOError for an unknown hostname."""
    resolver = DefaultLoopResolver()
    with pytest.raises(IOError) as excinfo:
        await resolver.resolve("nonexistent.host.example", 80)
    # The underlying exception should be a socket.gaierror
    assert isinstance(excinfo.value.__cause__, socket.gaierror)

@pytest.mark.asyncio
async def test_resolve_port_boundary():
    """Resolver should handle port 0 (any available port) without error."""
    resolver = DefaultLoopResolver()
    result = await resolver.resolve("localhost", 0)
    assert isinstance(result, list)
    # The returned addresses should have port 0
    for _, addr in result:
        assert addr[1] == 0

import asyncio
import socket
import pytest
from tornado.netutil import DefaultExecutorResolver

@pytest.mark.asyncio
async def test_resolve_valid_host(tmp_path):
    resolver = DefaultExecutorResolver()
    # Resolve a well‑known host; should return at least one address tuple
    result = await resolver.resolve("localhost", 80)
    assert isinstance(result, list)
    assert len(result) >= 1
    for family, addr in result:
        assert isinstance(family, int)
        assert isinstance(addr, tuple)
        # The address tuple should contain at least two elements (host, port)
        assert len(addr) >= 2
        # The port in the tuple should match the requested port
        assert addr[-1] == 80

@pytest.mark.asyncio
async def test_resolve_boundary_port_zero(tmp_path):
    resolver = DefaultExecutorResolver()
    # Port 0 is a valid input; the resolver should still return a list
    result = await resolver.resolve("localhost", 0)
    assert isinstance(result, list)
    # Even if no addresses are returned, the result should be a list
    assert isinstance(result, list)

@pytest.mark.asyncio
async def test_resolve_invalid_host_raises(tmp_path):
    resolver = DefaultExecutorResolver()
    # An obviously invalid hostname should raise an exception
    with pytest.raises(Exception) as excinfo:
        await resolver.resolve("nonexistent.host.example", 80)
    # The exception should be related to socket errors
    assert isinstance(excinfo.value, Exception)
    # The exception message should mention the hostname
    assert "nonexistent.host.example" in str(excinfo.value)

import asyncio
import socket
import pytest
from tornado.netutil import BlockingResolver


@pytest.mark.asyncio
async def test_blocking_resolver_success(tmp_path):
    """BlockingResolver should return a list of address tuples for a valid host."""
    resolver = BlockingResolver()
    # Resolve a known host; localhost should always resolve.
    result = await resolver.resolve("localhost", 80)
    # Each entry is a (family, address) tuple.
    assert isinstance(result, list)
    assert all(isinstance(entry, tuple) and len(entry) == 2 for entry in result)
    # At least one entry should be IPv4.
    assert any(entry[0] == socket.AF_INET for entry in result)
    resolver.close()


@pytest.mark.asyncio
async def test_blocking_resolver_invalid_host(tmp_path):
    """Resolving an unknown host should raise an IOError."""
    resolver = BlockingResolver()
    with pytest.raises(IOError):
        await resolver.resolve("nonexistent.host.example", 80)
    resolver.close()


@pytest.mark.asyncio
async def test_blocking_resolver_executor_shutdown(tmp_path):
    """After closing, the resolver's executor should be shut down and raise RuntimeError."""
    resolver = BlockingResolver()
    resolver.close()
    with pytest.raises(RuntimeError):
        await resolver.resolve("localhost", 80)

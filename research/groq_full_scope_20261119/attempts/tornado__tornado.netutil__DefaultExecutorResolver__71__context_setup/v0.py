import asyncio
import socket
import pytest
from tornado.netutil import DefaultExecutorResolver, _resolve_addr


@pytest.mark.asyncio
async def test_default_executor_resolver_resolves_known_host():
    """Resolver should return a non‑empty list for a known host."""
    resolver = DefaultExecutorResolver()
    result = await resolver.resolve("localhost", 80)
    assert isinstance(result, list)
    assert len(result) > 0
    # Each entry should be a tuple of (family, address)
    for fam, addr in result:
        assert isinstance(fam, int)
        assert isinstance(addr, tuple)
        # The address tuple should contain the host and port
        assert addr[0] in ("127.0.0.1", "::1")
        assert addr[1] == 80


def test_resolve_addr_returns_expected_family_and_address():
    """_resolve_addr should return the same families and addresses as socket.getaddrinfo."""
    # Use a port that is unlikely to be in /etc/services to trigger the special handling
    host = "localhost"
    port = 12345
    expected = socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM)
    expected_results = [(fam, addr) for fam, _, _, _, addr in expected]
    actual = _resolve_addr(host, port)
    assert actual == expected_results


@pytest.mark.asyncio
async def test_default_executor_resolver_raises_on_invalid_host():
    """Resolver should raise an IOError when the host cannot be resolved."""
    resolver = DefaultExecutorResolver()
    with pytest.raises(IOError):
        await resolver.resolve("nonexistent.host.example", 80)

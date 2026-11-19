import socket
import pytest
from tornado.netutil import BlockingResolver


def test_blocking_resolver_success(tmp_path):
    """BlockingResolver should return a list of address tuples for a valid host."""
    resolver = BlockingResolver()
    # Resolve localhost on an arbitrary port; we only care about the family/address format
    result = resolver.resolve("localhost", 80)
    # The result is a list of (family, address) tuples
    assert isinstance(result, list)
    assert all(isinstance(item, tuple) and len(item) == 2 for item in result)
    families, addresses = zip(*result)
    # All families should be either AF_INET or AF_INET6
    assert all(f in (socket.AF_INET, socket.AF_INET6) for f in families)
    # Addresses should be tuples suitable for socket.connect
    for addr in addresses:
        assert isinstance(addr, tuple)
        # For IPv4, address is (host, port); for IPv6, it is (host, port, flowinfo, scopeid)
        if isinstance(addr[0], str):
            assert isinstance(addr[1], int)
            if len(addr) == 4:
                assert isinstance(addr[2], int) and isinstance(addr[3], int)


def test_blocking_resolver_invalid_host(tmp_path):
    """Resolving an unknown host should raise an IOError."""
    resolver = BlockingResolver()
    with pytest.raises(IOError):
        resolver.resolve("nonexistent.host.example", 80)


def test_blocking_resolver_close_executor(tmp_path):
    """Closing the resolver should shut down its executor."""
    resolver = BlockingResolver()
    # The executor is a dummy_executor by default; we replace it with a real ThreadPoolExecutor
    import concurrent.futures
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    resolver.initialize(executor=executor, close_executor=True)
    # Resolve a host to ensure the executor is used
    resolver.resolve("localhost", 80)
    # Close the resolver; the executor should be shutdown
    resolver.close()
    assert executor._shutdown is True

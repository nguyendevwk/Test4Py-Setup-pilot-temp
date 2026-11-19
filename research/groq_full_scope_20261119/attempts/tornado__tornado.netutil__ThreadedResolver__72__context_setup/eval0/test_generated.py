import os
import socket
import concurrent.futures
import pytest
from tornado.netutil import ThreadedResolver, _resolve_addr

# ---------------------------------------------------------------------------

def test_threadpool_reuse_same_pid(tmp_path):
    """ThreadedResolver should reuse the same ThreadPoolExecutor within the same process."""
    # Create two resolvers with different thread counts
    r1 = ThreadedResolver()
    r1.initialize(num_threads=2)
    r2 = ThreadedResolver()
    r2.initialize(num_threads=5)

    # The underlying executor should be the same instance
    assert r1.executor is r2.executor
    # The pool should have the size of the first created pool (2 threads)
    assert isinstance(r1.executor, concurrent.futures.ThreadPoolExecutor)
    assert r1.executor._max_workers == 2
    # Closing one resolver should not shutdown the executor because close_executor=False
    r1.close()
    assert r1.executor is not None
    # The executor should still be usable by the second resolver
    assert r2.executor._max_workers == 2
    r2.close()
    # After both are closed, the executor should still exist (not shutdown)
    assert r2.executor is not None

# ---------------------------------------------------------------------------

def test_resolve_returns_expected_address(tmp_path):
    """ThreadedResolver.resolve should return a list of (family, address) tuples."""
    resolver = ThreadedResolver()
    resolver.initialize(num_threads=3)
    # Resolve a known host (localhost) on a common port
    result = resolver.resolve("localhost", 80, socket.AF_INET)
    # The result should be a list of tuples
    assert isinstance(result, list)
    assert all(isinstance(item, tuple) and len(item) == 2 for item in result)
    # Each tuple should contain a valid address family and an address tuple
    for fam, addr in result:
        assert fam == socket.AF_INET
        assert isinstance(addr, tuple)
        # The address tuple should be (host, port)
        assert addr[1] == 80
    resolver.close()

# ---------------------------------------------------------------------------

def test_resolve_invalid_host_raises_error(tmp_path):
    """Resolving an invalid hostname should raise an IOError."""
    resolver = ThreadedResolver()
    resolver.initialize(num_threads=1)
    with pytest.raises(IOError):
        resolver.resolve("nonexistent.host.example", 80, socket.AF_INET)
    resolver.close()

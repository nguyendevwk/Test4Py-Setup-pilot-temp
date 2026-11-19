import os
import socket
import concurrent.futures
import pytest
from tornado.netutil import ThreadedResolver, _resolve_addr

def test_threadpool_singleton_and_pid_behavior():
    # Create first resolver with 2 threads
    resolver1 = ThreadedResolver()
    resolver1.initialize(num_threads=2)
    pool1 = resolver1.executor
    assert isinstance(pool1, concurrent.futures.ThreadPoolExecutor)
    assert pool1._max_workers == 2

    # Creating a second resolver should reuse the same pool
    resolver2 = ThreadedResolver()
    resolver2.initialize(num_threads=5)  # different number should be ignored
    pool2 = resolver2.executor
    assert pool1 is pool2
    assert pool2._max_workers == 2  # still 2, not 5

    # Simulate a fork by manually changing the stored pid
    original_pid = ThreadedResolver._threadpool_pid
    ThreadedResolver._threadpool_pid = original_pid + 1  # pretend we forked
    resolver3 = ThreadedResolver()
    resolver3.initialize(num_threads=3)
    pool3 = resolver3.executor
    assert pool3 is not pool1  # new pool created
    assert pool3._max_workers == 3
    # Restore original pid for cleanliness
    ThreadedResolver._threadpool_pid = original_pid

def test_resolve_localhost_returns_ipv4_and_ipv6():
    resolver = ThreadedResolver()
    resolver.initialize(num_threads=1)
    # Resolve localhost on a common port (e.g., 80)
    results = resolver.resolve("localhost", 80, socket.AF_UNSPEC)
    # Resolve returns a Future-like awaitable; get result synchronously
    resolved = results.result()
    families = {fam for fam, _ in resolved}
    # Expect at least IPv4 and IPv6 addresses
    assert socket.AF_INET in families
    assert socket.AF_INET6 in families
    # Each address tuple should contain the host and port
    for fam, addr in resolved:
        if fam == socket.AF_INET:
            assert isinstance(addr, tuple) and len(addr) == 2
            assert addr[1] == 80
        elif fam == socket.AF_INET6:
            assert isinstance(addr, tuple) and len(addr) == 4
            assert addr[1] == 80

def test_resolve_invalid_host_raises_ioerror():
    resolver = ThreadedResolver()
    resolver.initialize(num_threads=1)
    # Resolve an obviously invalid hostname; should raise IOError
    with pytest.raises(IOError):
        resolver.resolve("nonexistent.host.example", 80).result()

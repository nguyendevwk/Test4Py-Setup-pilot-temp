import os
import concurrent.futures
import pytest
from tornado.netutil import ThreadedResolver


def test_threadpool_creation_and_size():
    """ThreadedResolver creates a ThreadPoolExecutor with the requested size."""
    resolver = ThreadedResolver()
    resolver.initialize(num_threads=5)
    pool = ThreadedResolver._threadpool
    assert isinstance(pool, concurrent.futures.ThreadPoolExecutor)
    # The executor should have the requested number of workers.
    assert pool._max_workers == 5
    # The resolver should have an executor attribute pointing to the pool.
    assert getattr(resolver, "executor", None) is pool


def test_shared_threadpool_between_instances():
    """All ThreadedResolver instances share the same thread pool."""
    resolver1 = ThreadedResolver()
    resolver1.initialize(num_threads=3)
    pool1 = ThreadedResolver._threadpool

    resolver2 = ThreadedResolver()
    resolver2.initialize(num_threads=7)  # size argument should be ignored
    pool2 = ThreadedResolver._threadpool

    # The same pool object should be reused.
    assert pool1 is pool2
    # The pool size should remain as set by the first instance.
    assert pool1._max_workers == 3
    # Both resolvers should reference the same executor.
    assert resolver1.executor is pool1
    assert resolver2.executor is pool1


def test_threadpool_reset_on_pid_change(monkeypatch):
    """If the process ID changes, the thread pool is reset."""
    original_getpid = os.getpid

    # Create a resolver with the current PID.
    resolver1 = ThreadedResolver()
    resolver1.initialize(num_threads=2)
    pool1 = ThreadedResolver._threadpool
    assert pool1 is not None

    # Simulate a fork by changing the PID returned by os.getpid.
    monkeypatch.setattr(os, "getpid", lambda: original_getpid() + 1)

    # Creating a new resolver should detect the PID change and create a new pool.
    resolver2 = ThreadedResolver()
    resolver2.initialize(num_threads=4)
    pool2 = ThreadedResolver._threadpool

    assert pool2 is not None
    assert pool2 is not pool1
    assert pool2._max_workers == 4

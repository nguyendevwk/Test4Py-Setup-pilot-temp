import os
import asyncio
import concurrent.futures
import pytest
from tornado.netutil import ThreadedResolver


def test_threadpool_reuse_same_pid():
    """ThreadedResolver should reuse the same ThreadPoolExecutor within the same process."""
    pool1 = ThreadedResolver._create_threadpool(5)
    pool2 = ThreadedResolver._create_threadpool(10)
    # The pool should be the same instance regardless of requested size
    assert pool1 is pool2
    # The pool should have the originally requested number of workers
    assert pool1._max_workers == 5
    # Subsequent calls with a larger size should not change the pool size
    assert pool2._max_workers == 5


def test_threadpool_recreated_after_fork():
    """After a fork, ThreadedResolver should create a new ThreadPoolExecutor."""
    parent_pool = ThreadedResolver._create_threadpool(3)
    pid_before = os.getpid()
    child_pid = os.fork()
    if child_pid == 0:
        # Child process
        child_pool = ThreadedResolver._create_threadpool(3)
        # The child pool should be a different instance
        assert child_pool is not parent_pool
        # The child pool should have the requested number of workers
        assert child_pool._max_workers == 3
        os._exit(0)
    else:
        # Parent process
        os.waitpid(child_pid, 0)
        # After the fork, the parent should still have its original pool
        assert ThreadedResolver._create_threadpool(3) is parent_pool


def test_initialize_sets_executor_and_closes_on_exit():
    """ThreadedResolver.initialize should set the executor and not close it automatically."""
    resolver = ThreadedResolver()
    resolver.initialize(num_threads=2)
    # The resolver's executor should be the shared thread pool
    assert isinstance(resolver.executor, concurrent.futures.ThreadPoolExecutor)
    assert resolver.executor._max_workers == 2
    # The executor should not be closed when the resolver is deleted
    resolver = None
    # The shared pool should still be alive
    pool = ThreadedResolver._create_threadpool(2)
    assert pool._max_workers == 2

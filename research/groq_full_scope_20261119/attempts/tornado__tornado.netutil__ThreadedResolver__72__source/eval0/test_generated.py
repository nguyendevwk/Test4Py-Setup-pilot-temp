import os
import concurrent.futures
import pytest
from tornado.netutil import ThreadedResolver

def test_single_threadpool_shared_across_instances():
    """ThreadedResolver should share the same ThreadPoolExecutor across instances."""
    resolver1 = ThreadedResolver()
    resolver1.initialize(num_threads=5)
    pool1 = resolver1.executor
    resolver2 = ThreadedResolver()
    resolver2.initialize(num_threads=5)
    pool2 = resolver2.executor
    assert pool1 is pool2, "Executors should be the same shared instance"
    assert isinstance(pool1, concurrent.futures.ThreadPoolExecutor)
    assert pool1._max_workers == 5

def test_threadpool_recreated_on_pid_change(monkeypatch):
    """If the process ID changes, the thread pool should be recreated."""
    resolver = ThreadedResolver()
    resolver.initialize(num_threads=3)
    original_pool = resolver.executor
    # Simulate a fork by changing the stored pid to a different value
    monkeypatch.setattr(ThreadedResolver, "_threadpool_pid", os.getpid() + 1)
    # Force recreation of the pool
    new_pool = ThreadedResolver._create_threadpool(3)
    assert new_pool is not original_pool, "Pool should be recreated when pid changes"
    assert isinstance(new_pool, concurrent.futures.ThreadPoolExecutor)
    assert new_pool._max_workers == 3

def test_initialize_sets_close_executor_false():
    """initialize should set close_executor to False on the base ExecutorResolver."""
    resolver = ThreadedResolver()
    resolver.initialize(num_threads=2)
    # The base class sets close_executor on the executor; we check the flag
    # by inspecting the executor's shutdown behavior (it should not close on resolver close)
    # Since we cannot directly access the flag, we ensure that calling close on resolver
    # does not shut down the shared pool by checking that the pool is still running.
    resolver.close()
    # The pool should still be alive; attempting to submit a task should succeed
    future = resolver.executor.submit(lambda: 42)
    assert future.result() == 42, "Executor should remain operational after resolver close"

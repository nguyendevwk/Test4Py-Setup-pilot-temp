import os
import concurrent.futures
import asyncio
import pytest
from tornado.netutil import ThreadedResolver

# Test 1: Creating a resolver initializes a thread pool with the requested size
def test_threaded_resolver_initializes_pool():
    resolver = ThreadedResolver()
    resolver.initialize(num_threads=5)
    # The executor should be a ThreadPoolExecutor with 5 workers
    assert isinstance(resolver.executor, concurrent.futures.ThreadPoolExecutor)
    assert resolver.executor._max_workers == 5

# Test 2: Multiple resolvers share the same thread pool within the same process
def test_threaded_resolver_shared_pool():
    resolver1 = ThreadedResolver()
    resolver1.initialize(num_threads=3)
    resolver2 = ThreadedResolver()
    resolver2.initialize(num_threads=7)  # size argument ignored after first pool
    # Both resolvers should reference the same executor instance
    assert resolver1.executor is resolver2.executor
    # The pool should still have the original size (3 workers)
    assert resolver1.executor._max_workers == 3

# Test 3: After a fork, the thread pool is recreated for the child process
def test_threaded_resolver_fork_behavior(tmp_path):
    # Create a resolver in the parent process
    parent_resolver = ThreadedResolver()
    parent_resolver.initialize(num_threads=2)
    parent_executor = parent_resolver.executor

    # Fork the process
    pid = os.fork()
    if pid == 0:
        # Child process
        try:
            child_resolver = ThreadedResolver()
            child_resolver.initialize(num_threads=4)
            child_executor = child_resolver.executor
            # In the child, the executor should be a new instance
            assert child_executor is not parent_executor
            # And it should have the requested number of workers
            assert child_executor._max_workers == 4
        finally:
            os._exit(0)
    else:
        # Parent process waits for child to finish
        _, status = os.waitpid(pid, 0)
        assert os.WIFEXITED(status) and os.WEXITSTATUS(status) == 0

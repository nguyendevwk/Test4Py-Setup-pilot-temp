import asyncio
import concurrent.futures
import socket
import pytest
from tornado.netutil import ExecutorResolver
from tornado.concurrent import run_on_executor

# Helper to run the resolver in the current event loop
async def run_resolver(resolver, host, port, family=socket.AF_UNSPEC):
    return await resolver.resolve(host, port, family)

@pytest.mark.asyncio
async def test_resolver_returns_valid_addresses(tmp_path):
    """ExecutorResolver should return a non‑empty list of address tuples for a valid host."""
    resolver = ExecutorResolver()
    resolver.initialize(concurrent.futures.ThreadPoolExecutor(max_workers=1))
    # Resolve localhost on an arbitrary port
    result = await run_resolver(resolver, "localhost", 80)
    # Each tuple should contain an address family and an address
    assert isinstance(result, list) and len(result) > 0
    for fam, addr in result:
        assert fam in (socket.AF_INET, socket.AF_INET6)
        assert isinstance(addr, tuple)
    resolver.close()
    # After close, executor should be None
    assert resolver.executor is None

@pytest.mark.asyncio
async def test_resolver_with_close_executor_false(tmp_path):
    """When close_executor is False, the executor should not be shut down on close."""
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    resolver = ExecutorResolver()
    resolver.initialize(executor=executor, close_executor=False)
    # Resolve a valid host
    result = await run_resolver(resolver, "localhost", 80)
    assert result  # non-empty
    # Close resolver but keep executor alive
    resolver.close()
    assert resolver.executor is None
    # Executor should still be running; we can submit a task
    future = executor.submit(lambda: 42)
    assert future.result() == 42
    executor.shutdown()

@pytest.mark.asyncio
async def test_resolver_invalid_host_raises(tmp_path):
    """Resolving an invalid hostname should raise a socket.gaierror."""
    resolver = ExecutorResolver()
    resolver.initialize(concurrent.futures.ThreadPoolExecutor(max_workers=1))
    with pytest.raises(socket.gaierror):
        await run_resolver(resolver, "nonexistent.host.example", 80)
    resolver.close()

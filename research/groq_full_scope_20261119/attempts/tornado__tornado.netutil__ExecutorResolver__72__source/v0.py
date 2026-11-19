import asyncio
import concurrent.futures
import socket
import pytest
from tornado.netutil import ExecutorResolver
from tornado.concurrent import dummy_executor

# Helper executor that records shutdown calls
class RecordingExecutor(concurrent.futures.ThreadPoolExecutor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shutdown_called = False

    def shutdown(self, *args, **kwargs):
        self.shutdown_called = True
        super().shutdown(*args, **kwargs)

@pytest.mark.asyncio
async def test_resolve_returns_expected_addresses():
    resolver = ExecutorResolver()
    resolver.initialize()
    # Resolve localhost on port 80 (common HTTP port)
    results = await resolver.resolve("localhost", 80)
    # Expect at least one address tuple
    assert isinstance(results, list) and len(results) >= 1
    # Each tuple should contain an address family and an address
    for family, addr in results:
        assert isinstance(family, int)
        assert isinstance(addr, tuple)
    # Clean up
    resolver.close()

@pytest.mark.asyncio
async def test_close_shuts_down_custom_executor():
    rec_exec = RecordingExecutor(max_workers=2)
    resolver = ExecutorResolver()
    resolver.initialize(executor=rec_exec, close_executor=True)
    # Resolve to trigger executor usage
    await resolver.resolve("localhost", 80)
    # Close resolver and check shutdown
    resolver.close()
    assert rec_exec.shutdown_called is True
    # Executor should be set to None after close
    assert resolver.executor is None

def test_default_dummy_executor_no_shutdown():
    resolver = ExecutorResolver()
    resolver.initialize()
    # The default executor should be dummy_executor
    assert resolver.executor is dummy_executor
    # Closing should not attempt to shutdown dummy_executor
    resolver.close()
    # dummy_executor has no shutdown attribute, so no exception should be raised
    assert resolver.executor is None

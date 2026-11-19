import asyncio
import concurrent.futures
import time
import pytest
from tornado.concurrent import run_on_executor, Future, chain_future

# Test 1: Decorator with default executor attribute
class WorkerDefault:
    def __init__(self):
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

    @run_on_executor
    def compute(self, x, y):
        # Simulate a blocking operation
        time.sleep(0.1)
        return x + y

@pytest.mark.asyncio
async def test_default_executor():
    worker = WorkerDefault()
    # The decorated method should return a Future that can be awaited
    fut = worker.compute(3, 4)
    assert isinstance(fut, Future)
    result = await fut
    assert result == 7
    # Ensure the method ran in the executor thread (not the main thread)
    assert fut.result() is not None

# Test 2: Decorator with custom executor attribute name
class WorkerCustom:
    def __init__(self):
        self._thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=1)

    @run_on_executor(executor='_thread_pool')
    def multiply(self, a, b):
        time.sleep(0.05)
        return a * b

@pytest.mark.asyncio
async def test_custom_executor():
    worker = WorkerCustom()
    fut = worker.multiply(6, 7)
    assert isinstance(fut, Future)
    result = await fut
    assert result == 42

# Test 3: Error when mixing positional and keyword arguments
def test_invalid_decorator_arguments():
    with pytest.raises(ValueError) as excinfo:
        @run_on_executor('positional', executor='kw')
        def dummy(self):
            pass
    assert "cannot combine positional and keyword args" in str(excinfo.value)

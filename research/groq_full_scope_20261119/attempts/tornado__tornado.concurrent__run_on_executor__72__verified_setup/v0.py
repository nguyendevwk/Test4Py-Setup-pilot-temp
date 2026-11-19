import asyncio
import concurrent.futures
import pytest
from tornado.concurrent import run_on_executor, Future, chain_future

# Test 1: normal usage – a method decorated with run_on_executor returns a Future
def test_run_on_executor_normal(tmp_path):
    class Worker:
        def __init__(self):
            self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

        @run_on_executor
        def compute(self, x, y):
            return x + y

    w = Worker()
    fut = w.compute(3, 4)
    assert isinstance(fut, Future)
    # Await the Future to get the result
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(fut)
    assert result == 7
    w.executor.shutdown(wait=True)

# Test 2: custom executor attribute name via keyword argument
def test_run_on_executor_custom_executor(tmp_path):
    class Worker:
        def __init__(self):
            self._pool = concurrent.futures.ThreadPoolExecutor(max_workers=1)

        @run_on_executor(executor="_pool")
        def multiply(self, a, b):
            return a * b

    w = Worker()
    fut = w.multiply(6, 7)
    assert isinstance(fut, Future)
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(fut)
    assert result == 42
    w._pool.shutdown(wait=True)

# Test 3: error handling – passing both positional and keyword arguments raises ValueError
def test_run_on_executor_invalid_args():
    with pytest.raises(ValueError) as excinfo:
        @run_on_executor(1, executor="foo")
        def dummy(self):
            return 1
    assert "cannot combine positional and keyword args" in str(excinfo.value)

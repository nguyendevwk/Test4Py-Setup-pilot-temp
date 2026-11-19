import asyncio
import concurrent.futures
import pytest
from tornado.concurrent import run_on_executor, Future, chain_future

class Dummy:
    def __init__(self):
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

    @run_on_executor
    def add(self, a, b):
        return a + b

    @run_on_executor(executor="_executor")
    def mul(self, a, b):
        return a * b

    _executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

@pytest.mark.asyncio
async def test_run_on_executor_normal():
    d = Dummy()
    result = await d.add(2, 3)
    assert result == 5
    # Ensure the underlying executor was used
    assert isinstance(d.executor, concurrent.futures.ThreadPoolExecutor)

@pytest.mark.asyncio
async def test_run_on_executor_custom_executor():
    d = Dummy()
    result = await d.mul(4, 5)
    assert result == 20
    assert isinstance(d._executor, concurrent.futures.ThreadPoolExecutor)

def test_run_on_executor_invalid_arguments():
    with pytest.raises(ValueError, match="cannot combine positional and keyword args"):
        run_on_executor(1, executor="foo")

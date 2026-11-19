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

    @run_on_executor(executor="_pool")
    def multiply(self, a, b):
        return a * b

    _pool = concurrent.futures.ThreadPoolExecutor(max_workers=1)


@pytest.mark.asyncio
async def test_run_on_executor_basic():
    d = Dummy()
    fut = d.add(2, 3)
    assert isinstance(fut, Future)
    result = await fut
    assert result == 5
    d.executor.shutdown(wait=True)


@pytest.mark.asyncio
async def test_run_on_executor_custom_executor():
    d = Dummy()
    fut = d.multiply(4, 5)
    assert isinstance(fut, Future)
    result = await fut
    assert result == 20
    d._pool.shutdown(wait=True)


def test_run_on_executor_invalid_arguments():
    with pytest.raises(ValueError, match="cannot combine positional and keyword args"):
        run_on_executor(1, executor="foo")
    with pytest.raises(ValueError, match="expected 1 argument"):
        run_on_executor(1, 2)

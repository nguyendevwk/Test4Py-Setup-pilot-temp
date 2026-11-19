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

    @run_on_executor(executor="executor")
    def multiply(self, a, b):
        return a * b

    @run_on_executor
    def raise_error(self):
        raise ValueError("boom")


@pytest.mark.asyncio
async def test_run_on_executor_normal():
    d = Dummy()
    fut = d.add(2, 3)
    assert isinstance(fut, Future)
    result = await fut
    assert result == 5


@pytest.mark.asyncio
async def test_run_on_executor_boundary_missing_executor():
    class NoExec:
        @run_on_executor
        def foo(self):
            return 42

    obj = NoExec()
    with pytest.raises(AttributeError):
        obj.foo()


@pytest.mark.asyncio
async def test_run_on_executor_error_propagation():
    d = Dummy()
    fut = d.raise_error()
    with pytest.raises(ValueError, match="boom"):
        await fut

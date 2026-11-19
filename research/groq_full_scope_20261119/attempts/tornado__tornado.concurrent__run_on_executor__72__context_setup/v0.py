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
    def fail(self):
        raise ValueError("boom")

    @run_on_executor
    def slow(self, delay):
        import time
        time.sleep(delay)
        return "done"


@pytest.mark.asyncio
async def test_run_on_executor_success():
    d = Dummy()
    fut = d.add(2, 3)
    assert isinstance(fut, Future)
    result = await fut
    assert result == 5


@pytest.mark.asyncio
async def test_run_on_executor_exception():
    d = Dummy()
    fut = d.fail()
    assert isinstance(fut, Future)
    with pytest.raises(ValueError, match="boom"):
        await fut


@pytest.mark.asyncio
async def test_run_on_executor_chain_and_timeout():
    d = Dummy()
    fut = d.slow(0.1)
    assert isinstance(fut, Future)
    # Ensure the future completes within a reasonable time
    result = await asyncio.wait_for(fut, timeout=1.0)
    assert result == "done"

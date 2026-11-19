import asyncio
import datetime
import pytest
from tornado.locks import Condition
from tornado import ioloop

@pytest.mark.asyncio
async def test_condition_notify_wakes_waiter():
    cond = Condition()
    # Start a waiter that will be notified
    waiter_task = asyncio.create_task(cond.wait())
    # Give the event loop a moment to schedule the waiter
    await asyncio.sleep(0)
    # Notify one waiter
    cond.notify()
    # The waiter should now be resolved with True
    result = await waiter_task
    assert result is True, "waiter should receive True after notify"

@pytest.mark.asyncio
async def test_condition_wait_timeout_returns_false():
    cond = Condition()
    # Wait with a very short timeout (1 ms)
    timeout = ioloop.IOLoop.current().time() + 0.001
    waiter_task = asyncio.create_task(cond.wait(timeout=timeout))
    # Give the event loop time to process the timeout
    await asyncio.sleep(0.01)
    result = await waiter_task
    assert result is False, "waiter should receive False after timeout"

@pytest.mark.asyncio
async def test_condition_notify_all_wakes_all_waiters():
    cond = Condition()
    # Create three waiters
    waiter_tasks = [asyncio.create_task(cond.wait()) for _ in range(3)]
    # Give the event loop a moment to schedule them
    await asyncio.sleep(0)
    # Notify all waiters
    cond.notify_all()
    # All waiters should now be resolved with True
    results = await asyncio.gather(*waiter_tasks)
    assert all(results), "all waiters should receive True after notify_all"

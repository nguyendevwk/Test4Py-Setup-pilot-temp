import asyncio
import datetime

import pytest
from tornado import ioloop
from tornado.locks import Condition


@pytest.mark.asyncio
async def test_wait_and_notify():
    """A waiter should receive True when notified."""
    condition = Condition()
    # Start a waiter that will be notified shortly
    waiter_task = asyncio.create_task(condition.wait())
    # Give the loop a moment to register the waiter
    await asyncio.sleep(0)
    # Notify one waiter
    condition.notify()
    # Await the waiter result
    result = await waiter_task
    assert result is True, "waiter should be notified with True"


@pytest.mark.asyncio
async def test_wait_timeout():
    """A waiter should receive False when the timeout expires."""
    condition = Condition()
    # Use a short timeout of 0.1 seconds
    timeout = ioloop.IOLoop.current().time() + 0.1
    waiter_task = asyncio.create_task(condition.wait(timeout=timeout))
    # Wait slightly longer than the timeout
    await asyncio.sleep(0.2)
    result = await waiter_task
    assert result is False, "waiter should time out and return False"


@pytest.mark.asyncio
async def test_notify_all_wakes_all_waiters():
    """notify_all should wake all pending waiters."""
    condition = Condition()
    # Create three waiters
    waiter1 = asyncio.create_task(condition.wait())
    waiter2 = asyncio.create_task(condition.wait())
    waiter3 = asyncio.create_task(condition.wait())
    # Ensure all waiters are registered
    await asyncio.sleep(0)
    # Notify all
    condition.notify_all()
    # Await all results
    results = await asyncio.gather(waiter1, waiter2, waiter3)
    assert all(results) is True, "All waiters should be notified with True"

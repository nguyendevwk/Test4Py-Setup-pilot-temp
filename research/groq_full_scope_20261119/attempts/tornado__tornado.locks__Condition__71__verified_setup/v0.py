import asyncio
import datetime
import threading
import time

import pytest
from tornado import ioloop
from tornado.locks import Condition


# Helper to run the tornado IOLoop in a background thread
@pytest.fixture(scope="module")
def ioloop_thread():
    loop = ioloop.IOLoop.current()
    thread = threading.Thread(target=loop.start, daemon=True)
    thread.start()
    # Give the loop a moment to start
    time.sleep(0.01)
    yield loop
    loop.add_callback(loop.stop)
    thread.join()


@pytest.mark.asyncio
async def test_condition_wait_and_notify(ioloop_thread):
    cond = Condition()
    # Start a waiter that will be notified
    waiter_task = asyncio.create_task(cond.wait())
    # Give the waiter a chance to register
    await asyncio.sleep(0.01)
    # Notify one waiter
    cond.notify()
    # Await the result
    result = await waiter_task
    assert result is True, "Waiter should receive True after notify"


@pytest.mark.asyncio
async def test_condition_timeout(ioloop_thread):
    cond = Condition()
    # Wait with a short timeout (absolute timestamp)
    timeout_ts = ioloop_thread.time() + 0.05
    waiter_task = asyncio.create_task(cond.wait(timeout=timeout_ts))
    # Do not notify; let the timeout expire
    result = await waiter_task
    assert result is False, "Waiter should receive False after timeout"


@pytest.mark.asyncio
async def test_condition_notify_all(ioloop_thread):
    cond = Condition()
    # Create multiple waiters
    waiter1 = asyncio.create_task(cond.wait())
    waiter2 = asyncio.create_task(cond.wait())
    waiter3 = asyncio.create_task(cond.wait())
    # Give them a moment to register
    await asyncio.sleep(0.01)
    # Notify all waiters
    cond.notify_all()
    # Await all results
    results = await asyncio.gather(waiter1, waiter2, waiter3)
    assert all(results), "All waiters should receive True after notify_all"

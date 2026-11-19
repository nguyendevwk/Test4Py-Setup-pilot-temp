import asyncio
import datetime
import threading
import time

import pytest
from tornado import ioloop
from tornado.locks import Condition


def _run_loop(coro):
    """Run an asyncio coroutine while the Tornado IOLoop is running."""
    loop = ioloop.IOLoop.current()
    result = None

    def target():
        nonlocal result
        result = asyncio.run(coro)

    t = threading.Thread(target=target)
    t.start()
    loop.start()
    t.join()
    return result


def test_condition_notify_immediately():
    """A waiter receives a notification when notify() is called before it awaits."""
    cond = Condition()

    async def waiter():
        return await cond.wait()

    # Notify before awaiting
    cond.notify()

    result = _run_loop(waiter())
    assert result is True, "wait() should return True when notified immediately"


def test_condition_timeout():
    """wait() returns False after the timeout expires without a notification."""
    cond = Condition()
    timeout_seconds = 0.1

    async def waiter():
        return await cond.wait(timeout=timeout_seconds)

    start = time.time()
    result = _run_loop(waiter())
    elapsed = time.time() - start
    assert result is False, "wait() should return False after timeout"
    assert elapsed >= timeout_seconds, "wait() should wait at least the timeout duration"


def test_condition_notify_all():
    """notify_all wakes all waiters, regardless of the number requested."""
    cond = Condition()
    results = []

    async def waiter(idx):
        res = await cond.wait()
        results.append((idx, res))

    async def runner():
        await asyncio.gather(*(waiter(i) for i in range(3)))
        cond.notify_all()

    _run_loop(runner())
    # All waiters should have been notified
    assert sorted(results) == [(0, True), (1, True), (2, True)]

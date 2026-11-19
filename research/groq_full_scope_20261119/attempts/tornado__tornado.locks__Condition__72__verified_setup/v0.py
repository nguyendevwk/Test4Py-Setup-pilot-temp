import asyncio
import datetime
import time

import pytest
from tornado import ioloop
from tornado.locks import Condition


def _run_loop_until(condition, stop_after: float = 2.0):
    """
    Helper that starts the IOLoop, runs until the given condition is true
    or the timeout expires, then stops the loop.
    """
    loop = ioloop.IOLoop.current()
    loop.add_timeout(loop.time() + stop_after, loop.stop)
    loop.start()


def test_wait_and_notify(tmp_path):
    """
    Verify that a waiter receives a notification and the returned Future
    resolves to True.
    """
    cond = Condition()
    waiter_future = cond.wait()

    def notifier():
        cond.notify()

    # Schedule notifier after a short delay
    ioloop.IOLoop.current().add_timeout(
        ioloop.IOLoop.current().time() + 0.1, notifier
    )

    _run_loop_until(lambda: waiter_future.done())

    assert waiter_future.done()
    assert waiter_future.result() is True


def test_timeout_behavior(tmp_path):
    """
    Verify that a waiter times out correctly and the returned Future
    resolves to False when no notification occurs.
    """
    cond = Condition()
    # Wait for 0.2 seconds
    timeout = datetime.timedelta(seconds=0.2)
    waiter_future = cond.wait(timeout=timeout)

    _run_loop_until(lambda: waiter_future.done(), stop_after=0.5)

    assert waiter_future.done()
    assert waiter_future.result() is False


def test_notify_all(tmp_path):
    """
    Verify that notify_all wakes all waiters and each Future resolves to True.
    """
    cond = Condition()
    futures = [cond.wait() for _ in range(3)]

    def notifier_all():
        cond.notify_all()

    ioloop.IOLoop.current().add_timeout(
        ioloop.IOLoop.current().time() + 0.1, notifier_all
    )

    _run_loop_until(lambda: all(f.done() for f in futures))

    for f in futures:
        assert f.done()
        assert f.result() is True

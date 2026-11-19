import asyncio
import concurrent.futures
import pytest
from tornado.concurrent import future_add_done_callback


def test_callback_called_immediately_for_done_concurrent_future():
    # Create a concurrent.futures.Future that is already done
    fut = concurrent.futures.Future()
    fut.set_result(42)

    called = {"count": 0, "future": None}

    def cb(f):
        called["count"] += 1
        called["future"] = f

    future_add_done_callback(fut, cb)

    # The callback should have been called exactly once
    assert called["count"] == 1
    # The callback should receive the same future instance
    assert called["future"] is fut
    # The future should still be done
    assert fut.done()
    assert fut.result() == 42


def test_callback_called_after_completion_asyncio_future():
    # Create an asyncio.Future that is not yet done
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    fut = asyncio.Future(loop=loop)

    called = {"count": 0, "future": None}

    def cb(f):
        called["count"] += 1
        called["future"] = f

    future_add_done_callback(fut, cb)

    # The callback should not have been called yet
    assert called["count"] == 0

    # Resolve the future
    fut.set_result("ok")
    # Run the event loop briefly to allow callbacks to fire
    loop.run_until_complete(asyncio.sleep(0))

    # Now the callback should have been called once
    assert called["count"] == 1
    assert called["future"] is fut
    assert fut.result() == "ok"

    loop.close()


def test_callback_receives_future_when_future_completes_after_registration():
    # Create a concurrent.futures.Future that will be completed later
    fut = concurrent.futures.Future()

    called = {"count": 0, "future": None}

    def cb(f):
        called["count"] += 1
        called["future"] = f

    future_add_done_callback(fut, cb)

    # The callback should not have been called yet
    assert called["count"] == 0

    # Complete the future
    fut.set_result("finished")

    # The callback should now be called
    assert called["count"] == 1
    assert called["future"] is fut
    assert fut.result() == "finished"

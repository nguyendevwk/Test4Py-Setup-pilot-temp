import asyncio
import concurrent.futures
import pytest
from tornado.concurrent import future_add_done_callback


def test_callback_called_immediately_for_done_concurrent_future():
    # Create a concurrent.futures.Future that is already finished
    fut = concurrent.futures.Future()
    fut.set_result(42)

    called = []

    def cb(f):
        called.append(f.result())

    future_add_done_callback(fut, cb)

    # The callback should have been called immediately with the result
    assert called == [42]


def test_callback_called_after_completion_for_concurrent_future():
    # Create a concurrent.futures.Future that is not yet finished
    fut = concurrent.futures.Future()

    called = []

    def cb(f):
        called.append(f.result())

    future_add_done_callback(fut, cb)

    # The callback should not have been called yet
    assert called == []

    # Complete the future
    fut.set_result(99)

    # Now the callback should have been invoked
    assert called == [99]


@pytest.mark.asyncio
async def test_callback_called_for_asyncio_future():
    # Create an asyncio.Future that is not yet finished
    fut = asyncio.Future()

    called = []

    def cb(f):
        called.append(f.result())

    future_add_done_callback(fut, cb)

    # The callback should not have been called yet
    assert called == []

    # Resolve the future
    fut.set_result("hello")

    # Await a tiny tick to allow callbacks to run
    await asyncio.sleep(0)

    # Now the callback should have been invoked
    assert called == ["hello"]

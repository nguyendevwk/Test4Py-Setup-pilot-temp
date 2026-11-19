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
    # The future should still be the same object
    assert fut.done()
    assert fut.result() == 42


def test_callback_called_after_completion_for_asyncio_future():
    # Create an asyncio.Future that is not yet finished
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    fut = loop.create_future()

    called = []

    def cb(f):
        called.append(f.result())

    future_add_done_callback(fut, cb)

    # The callback should not have been called yet
    assert called == []

    # Resolve the future
    fut.set_result("hello")
    # Run the loop briefly to allow callbacks to execute
    loop.run_until_complete(asyncio.sleep(0))

    # Now the callback should have been called
    assert called == ["hello"]
    assert fut.done()
    assert fut.result() == "hello"

    loop.close()


def test_callback_called_immediately_for_already_done_asyncio_future():
    # Create an asyncio.Future that is already finished
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    fut = loop.create_future()
    fut.set_result("world")

    called = []

    def cb(f):
        called.append(f.result())

    future_add_done_callback(fut, cb)

    # The callback should have been called immediately
    assert called == ["world"]
    assert fut.done()
    assert fut.result() == "world"

    loop.close()

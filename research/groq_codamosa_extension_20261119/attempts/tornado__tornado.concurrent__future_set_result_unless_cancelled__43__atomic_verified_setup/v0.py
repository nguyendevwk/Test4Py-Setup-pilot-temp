import asyncio
import concurrent.futures
import pytest
from tornado.concurrent import future_set_result_unless_cancelled


def test_future_set_result_unless_cancelled_sets_value_on_asyncio_future():
    """When the future is not cancelled, the value is set as its result."""
    loop = asyncio.new_event_loop()
    future = loop.create_future()
    future_set_result_unless_cancelled(future, 42)
    assert future.done()
    assert future.result() == 42
    loop.close()


def test_future_set_result_unless_cancelled_does_not_set_value_on_cancelled_future():
    """When the future is cancelled, the value is not set and no exception is raised."""
    loop = asyncio.new_event_loop()
    future = loop.create_future()
    future.cancel()
    future_set_result_unless_cancelled(future, 99)
    assert future.cancelled()
    with pytest.raises(asyncio.InvalidStateError):
        future.result()
    loop.close()


def test_future_set_result_unless_cancelled_raises_on_already_done_future():
    """If the future is already done (but not cancelled), set_result raises an exception."""
    loop = asyncio.new_event_loop()
    future = loop.create_future()
    future.set_result("initial")
    with pytest.raises(asyncio.InvalidStateError):
        future_set_result_unless_cancelled(future, "new")
    loop.close()

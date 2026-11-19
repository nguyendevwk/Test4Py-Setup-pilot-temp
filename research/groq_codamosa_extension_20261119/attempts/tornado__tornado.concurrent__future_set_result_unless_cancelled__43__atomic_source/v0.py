import asyncio
import concurrent.futures
import pytest
from tornado.concurrent import future_set_result_unless_cancelled


def test_future_set_result_unless_cancelled_sets_value_on_active_future():
    """When the future is not cancelled, the value is set as the result."""
    fut = asyncio.Future()
    future_set_result_unless_cancelled(fut, 42)
    assert fut.done()
    assert fut.result() == 42


def test_future_set_result_unless_cancelled_does_not_set_value_on_cancelled_future():
    """When the future is cancelled, the value is not set and no exception is raised."""
    fut = asyncio.Future()
    fut.cancel()
    future_set_result_unless_cancelled(fut, 99)
    assert fut.cancelled()
    with pytest.raises(asyncio.InvalidStateError):
        fut.result()


def test_future_set_result_unless_cancelled_raises_on_already_done_future():
    """If the future is already done (but not cancelled), set_result raises InvalidStateError."""
    fut = asyncio.Future()
    fut.set_result("initial")
    with pytest.raises(asyncio.InvalidStateError):
        future_set_result_unless_cancelled(fut, "new")

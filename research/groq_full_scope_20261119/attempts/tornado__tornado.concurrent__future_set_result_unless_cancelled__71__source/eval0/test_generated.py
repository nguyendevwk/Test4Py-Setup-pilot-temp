import asyncio
import concurrent.futures
import pytest
from tornado.concurrent import future_set_result_unless_cancelled


def test_set_result_on_active_future():
    """When the future is not cancelled, the value is set as its result."""
    fut = asyncio.Future()
    future_set_result_unless_cancelled(fut, 42)
    assert fut.done()
    assert fut.result() == 42


def test_no_result_on_cancelled_future():
    """If the future is cancelled, the function does nothing and does not raise."""
    fut = asyncio.Future()
    fut.cancel()
    future_set_result_unless_cancelled(fut, "ignored")
    assert fut.cancelled()
    with pytest.raises(asyncio.InvalidStateError):
        fut.result()


def test_invalid_state_when_future_already_done():
    """If the future already has a result, set_result raises InvalidStateError."""
    fut = asyncio.Future()
    fut.set_result("original")
    with pytest.raises(asyncio.InvalidStateError):
        future_set_result_unless_cancelled(fut, "new")

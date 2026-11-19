import asyncio
import concurrent.futures
import pytest
from tornado.concurrent import future_set_result_unless_cancelled

def test_future_set_result_unless_cancelled_sets_value_on_active_future():
    """When the future is not cancelled, the value is set as its result."""
    fut = asyncio.Future()
    future_set_result_unless_cancelled(fut, 42)
    assert fut.done()
    assert fut.result() == 42

def test_future_set_result_unless_cancelled_does_not_raise_on_cancelled_future():
    """When the future is cancelled, set_result is not called and no exception is raised."""
    fut = asyncio.Future()
    fut.cancel()
    # Calling the function should not raise an exception
    future_set_result_unless_cancelled(fut, "ignored")
    # The cancelled future should remain cancelled and have no result
    assert fut.cancelled()
    with pytest.raises(asyncio.InvalidStateError):
        fut.result()

def test_future_set_result_unless_cancelled_raises_on_already_done_future():
    """If the future already has a result, set_result raises InvalidStateError."""
    fut = asyncio.Future()
    fut.set_result("original")
    with pytest.raises(asyncio.InvalidStateError):
        future_set_result_unless_cancelled(fut, "new")

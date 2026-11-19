import asyncio
import concurrent.futures
import pytest
from tornado.concurrent import future_set_result_unless_cancelled

def test_future_set_result_when_not_cancelled():
    """When the future is not cancelled, the value is set as its result."""
    fut = asyncio.Future()
    future_set_result_unless_cancelled(fut, 42)
    assert fut.done()
    assert fut.result() == 42

def test_future_set_result_when_cancelled_does_not_raise():
    """If the future is cancelled, the function should not raise an exception."""
    fut = asyncio.Future()
    fut.cancel()
    # No exception should be raised
    future_set_result_unless_cancelled(fut, "ignored")
    # The future remains cancelled and has no result
    assert fut.cancelled()
    with pytest.raises(asyncio.InvalidStateError):
        fut.result()

def test_future_set_result_on_concurrent_future_and_already_done():
    """The function works with concurrent.futures.Future and raises when already done."""
    cfut = concurrent.futures.Future()
    # Set a result first
    cfut.set_result("initial")
    # Calling again should raise an InvalidStateError
    with pytest.raises(concurrent.futures.InvalidStateError):
        future_set_result_unless_cancelled(cfut, "new")
    # The result remains unchanged
    assert cfut.result() == "initial"

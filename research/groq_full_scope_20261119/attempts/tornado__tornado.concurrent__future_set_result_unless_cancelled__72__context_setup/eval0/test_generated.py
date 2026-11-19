import asyncio
import pytest
from tornado.concurrent import future_set_result_unless_cancelled
from concurrent import futures

def test_sets_result_when_not_cancelled():
    """When the future is not cancelled, the value is set as the result."""
    fut = asyncio.Future()
    future_set_result_unless_cancelled(fut, 42)
    assert fut.done()
    assert fut.result() == 42

def test_does_not_set_result_when_cancelled():
    """When the future is cancelled, the function does nothing and does not raise."""
    fut = asyncio.Future()
    fut.cancel()
    # No exception should be raised
    future_set_result_unless_cancelled(fut, "ignored")
    assert fut.cancelled()
    with pytest.raises(asyncio.InvalidStateError):
        fut.result()

def test_raises_when_future_already_done():
    """If the future already has a result, set_result will raise InvalidStateError."""
    fut = asyncio.Future()
    fut.set_result("initial")
    with pytest.raises(asyncio.InvalidStateError):
        future_set_result_unless_cancelled(fut, "new")

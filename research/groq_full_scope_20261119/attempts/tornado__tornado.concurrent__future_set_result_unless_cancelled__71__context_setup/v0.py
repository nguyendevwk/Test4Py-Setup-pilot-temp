import asyncio
import pytest
from concurrent import futures
from tornado.concurrent import future_set_result_unless_cancelled


def test_sets_result_when_not_cancelled():
    """When the future is not cancelled, the value is set as its result."""
    fut = asyncio.Future()
    future_set_result_unless_cancelled(fut, 42)
    assert fut.done()
    assert fut.result() == 42


def test_raises_invalid_state_error_if_future_already_has_result():
    """If the future already has a result, set_result will raise an exception."""
    fut = asyncio.Future()
    fut.set_result(10)
    with pytest.raises(asyncio.InvalidStateError):
        future_set_result_unless_cancelled(fut, 20)


def test_does_not_raise_when_future_is_cancelled():
    """When the future is cancelled, the function should not raise an exception."""
    fut = asyncio.Future()
    fut.cancel()
    # No exception should be raised, and the future remains cancelled
    future_set_result_unless_cancelled(fut, "ignored")
    assert fut.cancelled()
    with pytest.raises(asyncio.InvalidStateError):
        fut.result()

import asyncio
import pytest
from concurrent import futures
from tornado.concurrent import future_set_result_unless_cancelled
from asyncio import InvalidStateError


def test_future_set_result_unless_cancelled_sets_value_on_active_future():
    """When the future is not cancelled, the value is set as its result."""
    fut = asyncio.Future()
    future_set_result_unless_cancelled(fut, 42)
    assert fut.done()
    assert fut.result() == 42


def test_future_set_result_unless_cancelled_does_not_set_value_on_cancelled_future():
    """When the future is cancelled, the function does nothing and does not raise."""
    fut = asyncio.Future()
    fut.cancel()
    future_set_result_unless_cancelled(fut, 99)
    assert fut.cancelled()
    with pytest.raises(InvalidStateError):
        fut.result()


def test_future_set_result_unless_cancelled_raises_on_already_done_future():
    """If the future already has a result, set_result will raise InvalidStateError."""
    fut = asyncio.Future()
    fut.set_result(1)
    with pytest.raises(InvalidStateError):
        future_set_result_unless_cancelled(fut, 2)

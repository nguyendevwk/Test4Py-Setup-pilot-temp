import asyncio
import pytest
from tornado.concurrent import future_set_result_unless_cancelled

# Test that a non‑cancelled future receives the result
def test_future_set_result_unless_cancelled_sets_value():
    fut = asyncio.Future()
    future_set_result_unless_cancelled(fut, 42)
    assert fut.done()
    assert fut.result() == 42

# Test that a cancelled future does not raise and remains cancelled
def test_future_set_result_unless_cancelled_ignores_cancelled():
    fut = asyncio.Future()
    fut.cancel()
    # Should not raise an exception
    future_set_result_unless_cancelled(fut, "ignored")
    assert fut.cancelled()
    with pytest.raises(asyncio.InvalidStateError):
        fut.result()

# Test that if the future is already finished with a result, set_result raises
def test_future_set_result_unless_cancelled_raises_if_already_done():
    fut = asyncio.Future()
    fut.set_result("original")
    with pytest.raises(asyncio.InvalidStateError):
        future_set_result_unless_cancelled(fut, "new")

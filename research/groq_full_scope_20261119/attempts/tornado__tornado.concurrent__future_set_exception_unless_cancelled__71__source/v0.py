import asyncio
import logging
import pytest
from tornado.concurrent import future_set_exception_unless_cancelled
from concurrent.futures import Future as CFuture

# Test 1: Normal future – exception is set
def test_future_set_exception_normal():
    fut = asyncio.Future()
    exc = ValueError("test error")
    future_set_exception_unless_cancelled(fut, exc)
    assert fut.done()
    assert fut.exception() is exc

# Test 2: Cancelled future – exception is logged, not set
def test_future_set_exception_cancelled(caplog):
    fut = asyncio.Future()
    fut.cancel()
    exc = RuntimeError("cancelled error")
    caplog.set_level(logging.ERROR)
    future_set_exception_unless_cancelled(fut, exc)
    # Future remains cancelled and has no exception
    assert fut.cancelled()
    assert fut.exception() is None
    # Log contains the expected message and exc_info
    assert any(
        "Exception after Future was cancelled" in record.message
        for record in caplog.records
    )
    # Ensure the logged exception is the one we passed
    assert any(
        isinstance(record.exc_info[1], RuntimeError)
        and str(record.exc_info[1]) == "cancelled error"
        for record in caplog.records
    )

# Test 3: Future already completed – set_exception raises InvalidStateError
def test_future_set_exception_already_done():
    fut = asyncio.Future()
    fut.set_result(42)
    exc = KeyError("already done")
    with pytest.raises(asyncio.InvalidStateError):
        future_set_exception_unless_cancelled(fut, exc)

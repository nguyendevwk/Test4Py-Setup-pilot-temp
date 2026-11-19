import asyncio
import concurrent.futures
import logging
import pytest
from tornado.concurrent import future_set_exception_unless_cancelled

# Test 1: Normal behavior – exception is set on a non‑cancelled Future
def test_future_set_exception_on_active_future(tmp_path):
    fut = asyncio.Future()
    exc = ValueError("test error")
    future_set_exception_unless_cancelled(fut, exc)
    assert fut.done()
    assert fut.exception() is exc

# Test 2: Cancelled Future – exception is logged, not set
def test_future_set_exception_on_cancelled_future(caplog):
    fut = asyncio.Future()
    fut.cancel()
    exc = RuntimeError("cancelled error")
    with caplog.at_level(logging.ERROR, logger="tornado"):
        future_set_exception_unless_cancelled(fut, exc)
    # Future should remain cancelled and have no exception
    assert fut.cancelled()
    assert fut.exception() is None
    # Log should contain the exception info
    assert any("Exception after Future was cancelled" in rec.message for rec in caplog.records)

# Test 3: Future already completed with a result – set_exception raises InvalidStateError
def test_future_set_exception_on_done_future():
    fut = asyncio.Future()
    fut.set_result(42)
    exc = KeyError("already done")
    with pytest.raises(asyncio.InvalidStateError):
        future_set_exception_unless_cancelled(fut, exc)

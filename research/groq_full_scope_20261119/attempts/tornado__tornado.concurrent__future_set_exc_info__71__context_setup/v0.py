import asyncio
import types
import pytest
from tornado.concurrent import future_set_exc_info, future_set_exception_unless_cancelled


def test_future_set_exc_info_sets_exception():
    """When a non‑cancelled Future receives an exception, it is set correctly."""
    fut = asyncio.Future()
    exc = ValueError("boom")
    exc_info = (ValueError, exc, None)
    future_set_exc_info(fut, exc_info)
    assert fut.done()
    assert fut.exception() is exc


def test_future_set_exc_info_noop_on_cancelled():
    """If the Future is already cancelled, future_set_exc_info does not raise."""
    fut = asyncio.Future()
    fut.cancel()
    exc = RuntimeError("should not be set")
    exc_info = (RuntimeError, exc, None)
    # No exception should be raised and the Future remains cancelled
    future_set_exc_info(fut, exc_info)
    assert fut.cancelled()
    assert fut.exception() is None


def test_future_set_exc_info_raises_on_missing_exception():
    """future_set_exc_info must raise if exc_info[1] is None."""
    fut = asyncio.Future()
    exc_info = (None, None, None)
    with pytest.raises(Exception, match="no exception"):
        future_set_exc_info(fut, exc_info)

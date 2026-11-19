import asyncio
import logging
import pytest
from concurrent import futures
from tornado.concurrent import future_set_exception_unless_cancelled
from tornado.log import app_log


def test_set_exception_on_active_future():
    """When the future is not cancelled, the exception is set."""
    fut = asyncio.Future()
    exc = ValueError("test error")
    future_set_exception_unless_cancelled(fut, exc)
    assert fut.exception() is exc
    assert fut.done()
    assert not fut.cancelled()


def test_log_and_no_exception_when_future_cancelled(tmp_path, caplog):
    """If the future is cancelled, the exception is logged and not set."""
    fut = asyncio.Future()
    fut.cancel()
    exc = RuntimeError("cancelled error")
    with caplog.at_level(logging.ERROR, logger=app_log.name):
        future_set_exception_unless_cancelled(fut, exc)
    # The future remains cancelled and has no exception
    assert fut.cancelled()
    assert fut.exception() is None
    # The log contains the expected message and exc_info
    assert any(
        "Exception after Future was cancelled" in record.message
        for record in caplog.records
    )
    # Ensure the exception is logged as exc_info
    assert any(record.exc_info[1] is exc for record in caplog.records)


def test_invalid_state_error_on_done_future():
    """If the future is already done with a result, set_exception raises."""
    fut = futures.Future()
    fut.set_result(42)
    exc = KeyError("already done")
    with pytest.raises(asyncio.InvalidStateError):
        future_set_exception_unless_cancelled(fut, exc)

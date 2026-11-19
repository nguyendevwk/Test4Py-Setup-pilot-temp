import asyncio
import types
import pytest
from tornado.concurrent import future_set_exc_info, future_set_exception_unless_cancelled

# Helper to create a standard exc_info tuple
def make_exc_info(exc: BaseException):
    return (type(exc), exc, exc.__traceback__)

def test_future_set_exc_info_sets_exception():
    """future_set_exc_info should set the exception on a pending Future."""
    loop = asyncio.new_event_loop()
    future = loop.create_future()
    exc = ValueError("test error")
    future_set_exc_info(future, make_exc_info(exc))
    assert future.done()
    assert future.exception() is exc
    loop.close()

def test_future_set_exc_info_noop_on_cancelled():
    """If the Future is cancelled, future_set_exc_info should be a no‑op."""
    loop = asyncio.new_event_loop()
    future = loop.create_future()
    future.cancel()
    exc = RuntimeError("ignored")
    future_set_exc_info(future, make_exc_info(exc))
    # The future remains cancelled and no exception is set
    assert future.cancelled()
    assert future.exception() is None
    loop.close()

def test_future_set_exc_info_raises_on_missing_exception():
    """future_set_exc_info must raise if exc_info[1] is None."""
    loop = asyncio.new_event_loop()
    future = loop.create_future()
    with pytest.raises(Exception, match="no exception"):
        future_set_exc_info(future, (None, None, None))
    loop.close()

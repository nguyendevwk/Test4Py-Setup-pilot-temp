import asyncio
import types
import pytest
from tornado.concurrent import future_set_exc_info, future_set_exception_unless_cancelled


def test_set_exception_on_pending_future():
    """future_set_exc_info should set the exception on a pending Future."""
    loop = asyncio.new_event_loop()
    future = loop.create_future()
    exc = RuntimeError("test error")
    exc_info = (type(exc), exc, exc.__traceback__)

    future_set_exc_info(future, exc_info)

    assert future.done()
    assert future.exception() is exc
    loop.close()


def test_noop_when_future_already_cancelled():
    """If the Future is cancelled, future_set_exc_info should not raise."""
    loop = asyncio.new_event_loop()
    future = loop.create_future()
    future.cancel()
    exc = ValueError("cancelled error")
    exc_info = (type(exc), exc, exc.__traceback__)

    # No exception should be raised even though the Future is cancelled
    future_set_exc_info(future, exc_info)

    # The Future remains cancelled and no exception is set
    assert future.cancelled()
    assert future.exception() is None
    loop.close()


def test_exc_info_missing_raises_exception():
    """future_set_exc_info must raise if exc_info[1] is None."""
    loop = asyncio.new_event_loop()
    future = loop.create_future()
    exc_info = (None, None, None)

    with pytest.raises(Exception, match="no exception"):
        future_set_exc_info(future, exc_info)

    loop.close()

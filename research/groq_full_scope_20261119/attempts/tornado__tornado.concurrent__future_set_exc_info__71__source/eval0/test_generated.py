import asyncio
import concurrent.futures
import types
import pytest
from tornado.concurrent import future_set_exc_info

def test_future_set_exc_info_sets_exception_on_asyncio_future(tmp_path):
    """Verify that an asyncio.Future receives the exception from exc_info."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    fut = loop.create_future()
    exc = ValueError("asyncio error")
    exc_info = (ValueError, exc, None)
    future_set_exc_info(fut, exc_info)
    assert fut.done()
    assert fut.exception() is exc
    loop.close()

def test_future_set_exc_info_ignores_cancelled_future(tmp_path):
    """When the future is cancelled, future_set_exc_info should be a no-op."""
    fut = concurrent.futures.Future()
    fut.cancel()
    exc = RuntimeError("should not be set")
    exc_info = (RuntimeError, exc, None)
    future_set_exc_info(fut, exc_info)
    assert fut.cancelled()
    assert fut.exception() is None

def test_future_set_exc_info_raises_on_missing_exception(tmp_path):
    """future_set_exc_info must raise if exc_info[1] is None."""
    fut = asyncio.Future()
    exc_info = (None, None, None)
    with pytest.raises(Exception, match="no exception"):
        future_set_exc_info(fut, exc_info)

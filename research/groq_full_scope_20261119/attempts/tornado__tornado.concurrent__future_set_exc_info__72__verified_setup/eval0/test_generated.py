import asyncio
import types
import pytest
from tornado.concurrent import future_set_exc_info

def test_set_exception_on_pending_future():
    loop = asyncio.new_event_loop()
    try:
        fut = loop.create_future()
        exc = ValueError("test error")
        future_set_exc_info(fut, (type(exc), exc, exc.__traceback__))
        assert fut.done()
        assert fut.exception() is exc
    finally:
        loop.close()

def test_noop_on_cancelled_future():
    loop = asyncio.new_event_loop()
    try:
        fut = loop.create_future()
        fut.cancel()
        exc = RuntimeError("should not be set")
        future_set_exc_info(fut, (type(exc), exc, exc.__traceback__))
        assert fut.cancelled()
        assert fut.exception() is None
    finally:
        loop.close()

def test_raises_when_no_exception_provided():
    loop = asyncio.new_event_loop()
    try:
        fut = loop.create_future()
        with pytest.raises(Exception, match="no exception"):
            future_set_exc_info(fut, (None, None, None))
    finally:
        loop.close()

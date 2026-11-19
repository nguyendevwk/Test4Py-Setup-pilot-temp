import asyncio
import pytest
from concurrent import futures
from tornado.concurrent import Future as TornadoFuture
from tornado.concurrent import future_add_done_callback


def test_callback_invoked_when_future_completes():
    """The callback should be called when a concurrent Future completes."""
    loop = asyncio.new_event_loop()
    future = futures.Future()
    called = []

    def cb(fut):
        called.append(fut)

    future_add_done_callback(future, cb)
    future.set_result(42)

    assert called == [future]
    assert called[0].result() == 42


def test_callback_called_immediately_if_future_already_done():
    """If the future is already done, the callback should be invoked immediately."""
    future = futures.Future()
    future.set_result("done")
    called = []

    def cb(fut):
        called.append(fut)

    future_add_done_callback(future, cb)

    assert called == [future]
    assert called[0].result() == "done"


def test_callback_with_tornado_future_and_exception():
    """The function should work with Tornado's Future and propagate exceptions."""
    future = TornadoFuture()
    called = []

    def cb(fut):
        called.append(fut)

    future_add_done_callback(future, cb)
    future.set_exception(ValueError("boom"))

    assert called == [future]
    with pytest.raises(ValueError, match="boom"):
        future.result()

import asyncio
import concurrent.futures
import pytest
from tornado.concurrent import future_add_done_callback


def test_callback_invoked_after_future_completion(tmp_path):
    """When the future is not yet done, the callback is called after completion."""
    future = concurrent.futures.Future()
    called = []

    def callback(fut):
        called.append(fut)

    future_add_done_callback(future, callback)
    assert called == []  # not called yet

    future.set_result("ok")
    assert called == [future]
    assert called[0].result() == "ok"


def test_callback_invoked_immediately_if_future_done(tmp_path):
    """If the future is already done, the callback is invoked immediately."""
    future = concurrent.futures.Future()
    future.set_result(42)
    called = []

    def callback(fut):
        called.append(fut)

    future_add_done_callback(future, callback)
    assert called == [future]
    assert called[0].result() == 42


def test_invalid_future_raises_attribute_error(tmp_path):
    """Passing an object without a `done` method raises AttributeError."""
    class Dummy:
        pass

    dummy = Dummy()
    with pytest.raises(AttributeError):
        future_add_done_callback(dummy, lambda f: None)

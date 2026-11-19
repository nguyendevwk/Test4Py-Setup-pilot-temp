import asyncio
import concurrent.futures
import pytest
from tornado.concurrent import future_add_done_callback

def test_callback_called_after_completion(tmp_path):
    """The callback should be invoked once the future finishes."""
    loop = asyncio.new_event_loop()
    future = loop.create_future()
    called = []

    def cb(fut):
        called.append(fut)

    future_add_done_callback(future, cb)
    loop.call_soon_threadsafe(future.set_result, 42)
    loop.run_until_complete(future)
    loop.close()

    assert called, "Callback was not called"
    assert called[0] is future, "Callback received wrong future"
    assert future.result() == 42, "Future did not complete correctly"

def test_callback_called_immediately_when_done(tmp_path):
    """If the future is already done, the callback should be called immediately."""
    future = concurrent.futures.Future()
    future.set_result("done")
    called = []

    def cb(fut):
        called.append(fut)

    future_add_done_callback(future, cb)

    assert called, "Callback was not called immediately"
    assert called[0] is future, "Callback received wrong future"
    assert future.result() == "done", "Future result mismatch"

def test_callback_receives_future_and_can_raise(tmp_path):
    """The callback receives the future and may raise an exception."""
    future = concurrent.futures.Future()
    future.set_result(1)

    def cb(fut):
        assert fut is future, "Callback did not receive the correct future"
        raise RuntimeError("callback error")

    with pytest.raises(RuntimeError, match="callback error"):
        future_add_done_callback(future, cb)

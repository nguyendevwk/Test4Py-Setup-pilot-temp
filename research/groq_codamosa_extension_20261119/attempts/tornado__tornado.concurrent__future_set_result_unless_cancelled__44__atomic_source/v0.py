import asyncio
import concurrent.futures
import pytest
from tornado.concurrent import future_set_result_unless_cancelled


def test_sets_result_on_non_cancelled_asyncio_future():
    loop = asyncio.new_event_loop()
    future = loop.create_future()
    future_set_result_unless_cancelled(future, 42)
    assert future.done()
    assert future.result() == 42
    loop.close()


def test_does_not_set_result_on_cancelled_asyncio_future():
    loop = asyncio.new_event_loop()
    future = loop.create_future()
    future.cancel()
    future_set_result_unless_cancelled(future, 99)
    assert future.cancelled()
    with pytest.raises(asyncio.InvalidStateError):
        future.result()
    loop.close()


def test_works_with_concurrent_futures_future():
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    future = executor.submit(lambda: None)  # create a Future that is already done
    # Cancel the future to simulate a cancelled state
    future.cancel()
    future_set_result_unless_cancelled(future, "hello")
    # Since it was cancelled, the result should remain unset and cancelled flag true
    assert future.cancelled()
    with pytest.raises(concurrent.futures.CancelledError):
        future.result()
    executor.shutdown()

import sys
import pytest
from concurrent import futures
from tornado.concurrent import DummyExecutor, future_set_result_unless_cancelled, future_set_exception_unless_cancelled

def test_dummy_executor_success():
    """Submitting a simple function returns a Future with the correct result."""
    executor = DummyExecutor()
    future = executor.submit(lambda x, y: x + y, 2, 3)
    assert isinstance(future, futures.Future)
    assert future.done()
    assert not future.cancelled()
    assert future.result() == 5

def test_dummy_executor_exception():
    """If the submitted function raises, the Future holds the exception."""
    executor = DummyExecutor()
    def raise_error():
        raise ValueError("boom")
    future = executor.submit(raise_error)
    assert isinstance(future, futures.Future)
    assert future.done()
    assert future.cancelled() is False
    with pytest.raises(ValueError) as excinfo:
        future.result()
    assert str(excinfo.value) == "boom"

def test_dummy_executor_shutdown_noop():
    """shutdown() on DummyExecutor should be a no-op and not raise."""
    executor = DummyExecutor()
    # Ensure shutdown can be called with both signatures
    if sys.version_info >= (3, 9):
        executor.shutdown(wait=True, cancel_futures=False)
    else:
        executor.shutdown(wait=True)
    # No exception should be raised and executor remains usable
    future = executor.submit(lambda: 42)
    assert future.result() == 42

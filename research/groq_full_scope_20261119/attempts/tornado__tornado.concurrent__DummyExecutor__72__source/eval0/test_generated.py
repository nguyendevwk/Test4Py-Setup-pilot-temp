import sys
import pytest
from concurrent import futures
from tornado.concurrent import DummyExecutor


def test_dummy_executor_success(tmp_path):
    """Submitting a simple function should return a Future with the correct result."""
    executor = DummyExecutor()
    future = executor.submit(lambda x, y: x + y, 2, 3)
    assert isinstance(future, futures.Future)
    assert future.done()
    assert not future.cancelled()
    assert future.result() == 5


def test_dummy_executor_exception(tmp_path):
    """If the function raises, the Future should contain the exception."""
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


def test_dummy_executor_shutdown(tmp_path):
    """Calling shutdown should not raise an exception regardless of Python version."""
    executor = DummyExecutor()
    # The shutdown signature differs between Python 3.9+ and older versions.
    if sys.version_info >= (3, 9):
        # Should accept both arguments without error.
        executor.shutdown(wait=True, cancel_futures=False)
        executor.shutdown(wait=False, cancel_futures=True)
    else:
        # Should accept only the wait argument.
        executor.shutdown(wait=True)
        executor.shutdown(wait=False)

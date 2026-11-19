import pytest
import concurrent.futures
from tornado.concurrent import DummyExecutor, future_set_exception_unless_cancelled


def test_dummy_executor_successful_submission():
    """Submitting a simple function returns a Future that resolves to the expected value."""
    executor = DummyExecutor()
    future = executor.submit(lambda x, y: x + y, 2, 3)
    assert isinstance(future, concurrent.futures.Future)
    # The Future should already be done and contain the correct result
    assert future.done()
    assert future.result() == 5


def test_dummy_executor_exception_propagation():
    """If the submitted function raises, the Future should contain that exception."""
    executor = DummyExecutor()

    def raise_error():
        raise ValueError("boom")

    future = executor.submit(raise_error)
    assert future.done()
    with pytest.raises(ValueError) as excinfo:
        future.result()
    assert str(excinfo.value) == "boom"


def test_dummy_executor_future_not_cancelled_on_submission():
    """A Future created by DummyExecutor should not be cancelled immediately after submission."""
    executor = DummyExecutor()
    future = executor.submit(lambda: "ok")
    # The Future should not be cancelled; cancel() would return False
    assert not future.cancelled()
    # Canceling after submission should succeed
    assert future.cancel()
    # After cancellation, the Future remains cancelled and has no result
    assert future.cancelled()
    with pytest.raises(concurrent.futures.CancelledError):
        future.result()

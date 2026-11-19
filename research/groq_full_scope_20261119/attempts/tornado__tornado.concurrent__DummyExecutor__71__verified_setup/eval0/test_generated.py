import pytest
import sys
import types
from concurrent import futures

# Import the target class from the module under test
from tornado.concurrent import DummyExecutor


def test_dummy_executor_success():
    """Submitting a normal function returns a future with the correct result."""
    executor = DummyExecutor()
    # A simple function that returns a value
    def add(a, b):
        return a + b

    future = executor.submit(add, 2, 3)
    # The future should be immediately done
    assert future.done()
    # The result should match the function output
    assert future.result() == 5
    # No exception should be stored
    assert future.exception() is None


def test_dummy_executor_exception():
    """Submitting a function that raises an exception stores the exception."""
    executor = DummyExecutor()
    # A function that raises a ValueError
    def fail():
        raise ValueError("boom")

    future = executor.submit(fail)
    assert future.done()
    # The future should contain the exception
    exc = future.exception()
    assert isinstance(exc, ValueError)
    assert str(exc) == "boom"
    # result() should raise the stored exception
    with pytest.raises(ValueError):
        future.result()


def test_dummy_executor_shutdown_noop():
    """Calling shutdown on DummyExecutor should be a no‑op and not raise."""
    executor = DummyExecutor()
    # Submit a simple task to ensure executor is usable
    future = executor.submit(lambda: "ok")
    assert future.result() == "ok"

    # shutdown should accept both signatures depending on Python version
    if sys.version_info >= (3, 9):
        # New signature: wait and cancel_futures
        executor.shutdown(wait=True, cancel_futures=False)
    else:
        executor.shutdown(wait=True)

    # After shutdown, the executor should still function
    future2 = executor.submit(lambda: 42)
    assert future2.result() == 42

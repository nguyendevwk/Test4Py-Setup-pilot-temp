import sys
import pytest
from concurrent import futures
from tornado.concurrent import DummyExecutor


def test_dummy_executor_success():
    """Submitting a simple function returns a Future with the correct result."""
    executor = DummyExecutor()
    future = executor.submit(lambda x, y: x + y, 2, 3)
    assert isinstance(future, futures.Future)
    assert future.done()
    assert not future.cancelled()
    assert future.result() == 5


def test_dummy_executor_exception():
    """If the submitted function raises, the Future contains the exception."""
    executor = DummyExecutor()

    def raise_error():
        raise ValueError("boom")

    future = executor.submit(raise_error)
    assert future.done()
    assert future.exception() is not None
    assert isinstance(future.exception(), ValueError)
    assert str(future.exception()) == "boom"


def test_dummy_executor_cancel_behavior():
    """A Future returned by DummyExecutor cannot be cancelled after submission."""
    executor = DummyExecutor()
    future = executor.submit(lambda: 42)
    # Attempt to cancel after the task has already run
    cancelled = future.cancel()
    assert cancelled is False
    assert future.done()
    assert future.result() == 42

import sys
import pytest
from concurrent import futures
from tornado.concurrent import DummyExecutor

# Test 1: Normal function execution
def test_dummy_executor_success():
    executor = DummyExecutor()
    # A simple function that returns a value
    def add(a, b):
        return a + b

    future = executor.submit(add, 2, 3)
    # The future should be done and contain the correct result
    assert future.done()
    assert future.result() == 5

# Test 2: Function that raises an exception
def test_dummy_executor_exception():
    executor = DummyExecutor()
    # A function that raises a ValueError
    def fail():
        raise ValueError("boom")

    future = executor.submit(fail)
    # The future should be done and contain the exception
    assert future.done()
    with pytest.raises(ValueError) as excinfo:
        future.result()
    assert str(excinfo.value) == "boom"

# Test 3: Shutdown method does not raise and is a no-op
def test_dummy_executor_shutdown():
    executor = DummyExecutor()
    # Calling shutdown should not raise an exception
    try:
        executor.shutdown()
    except Exception as e:
        pytest.fail(f"shutdown raised an exception: {e}")
    # After shutdown, submit should still work
    def identity(x):
        return x
    future = executor.submit(identity, 42)
    assert future.result() == 42

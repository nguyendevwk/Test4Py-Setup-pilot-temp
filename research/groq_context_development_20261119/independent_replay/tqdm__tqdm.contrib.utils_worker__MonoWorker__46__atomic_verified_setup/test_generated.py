import time
import pytest
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from tqdm.contrib.utils_worker import MonoWorker


def test_single_task_execution():
    """Submitting a single task should execute and return its result."""
    worker = MonoWorker()

    def add(a, b):
        return a + b

    future = worker.submit(add, 2, 3)
    assert future is not None
    result = future.result(timeout=1)
    assert result == 5


def test_task_replacement_and_cancellation():
    """Submitting more than two tasks should keep the running task and cancel the waiting one."""
    worker = MonoWorker()

    def long_task():
        time.sleep(0.5)
        return "long"

    def short_task():
        return "short"

    # Submit first task (will run)
    f1 = worker.submit(long_task)
    # Submit second task (will wait)
    f2 = worker.submit(short_task)
    # Submit third task (should replace waiting task)
    f3 = worker.submit(short_task)

    # f2 should be cancelled
    assert f2.cancelled() is True
    # f1 should still be running
    assert f1.running() is True
    # f3 should be the waiting task
    assert f3.running() is False
    # Wait for the long task to finish
    result = f1.result(timeout=1)
    assert result == "long"
    # f3 should complete after f1 finishes
    result3 = f3.result(timeout=1)
    assert result3 == "short"


def test_task_exception_propagation():
    """If a submitted task raises an exception, the future should contain that exception."""
    worker = MonoWorker()

    def faulty():
        raise ValueError("boom")

    future = worker.submit(faulty)
    with pytest.raises(ValueError, match="boom"):
        future.result(timeout=1)

import time
import pytest
from collections import deque
from concurrent.futures import ThreadPoolExecutor, Future
from tqdm.contrib.utils_worker import MonoWorker


def test_single_task_execution():
    """Submitting a single task should run it and return a Future."""
    worker = MonoWorker()
    result_container = []

    def task():
        result_container.append("done")

    future = worker.submit(task)
    assert isinstance(future, Future)
    # Wait for completion
    future.result(timeout=1)
    assert result_container == ["done"]


def test_waiting_task_replacement():
    """Submitting a second task should replace the waiting one when the queue is full."""
    worker = MonoWorker()
    order = []

    def first():
        # Sleep to keep it running
        time.sleep(0.2)
        order.append("first")

    def second():
        order.append("second")

    # Submit first task (running)
    f1 = worker.submit(first)
    # Submit second task (waiting)
    f2 = worker.submit(second)
    # Submit third task (should replace second)
    f3 = worker.submit(lambda: order.append("third"))

    # Wait for all to finish
    f1.result(timeout=1)
    f2.result(timeout=1)
    f3.result(timeout=1)

    # The second task should not have executed
    assert order == ["first", "third"]


def test_task_exception_propagation():
    """A task that raises an exception should have that exception in its Future."""
    worker = MonoWorker()

    def bad_task():
        raise ValueError("boom")

    future = worker.submit(bad_task)
    with pytest.raises(ValueError, match="boom"):
        future.result()

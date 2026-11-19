import time
import pytest
from collections import deque
from concurrent.futures import ThreadPoolExecutor, Future
from tqdm.contrib.utils_worker import MonoWorker


def test_single_task_runs_and_completes():
    """Submitting a single task should run and complete."""
    worker = MonoWorker()
    result_container = []

    def task():
        time.sleep(0.1)
        result_container.append("done")

    future = worker.submit(task)
    assert isinstance(future, Future)
    # Wait for completion
    future.result(timeout=1)
    assert result_container == ["done"]
    assert future.done()
    # After completion, the deque should be empty
    assert len(worker.futures) == 0


def test_waiting_task_replaced_by_latest_submission():
    """The most recent submission should replace any waiting task."""
    worker = MonoWorker()
    order = []

    def long_task():
        time.sleep(0.2)
        order.append("long")

    def short_task():
        time.sleep(0.05)
        order.append("short")

    # Submit long task first
    long_future = worker.submit(long_task)
    # Immediately submit short task, which should replace the waiting one
    short_future = worker.submit(short_task)

    # The deque should contain only the running long task
    assert len(worker.futures) == 1
    assert worker.futures[0] is long_future
    assert not short_future.done()  # short task was cancelled

    # Wait for the long task to finish
    long_future.result(timeout=1)
    assert order == ["long"]


def test_submission_of_failing_task_does_not_append_future():
    """If the submitted function raises, no Future should be appended."""
    worker = MonoWorker()
    counter = 0

    def failing_task():
        nonlocal counter
        counter += 1
        raise ValueError("intentional failure")

    future = worker.submit(failing_task)
    # The submit method catches the exception and does not return a Future
    assert future is None
    # The counter should have incremented once
    assert counter == 1
    # The deque should remain empty
    assert len(worker.futures) == 0

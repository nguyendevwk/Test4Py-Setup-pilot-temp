import time
import pytest
from collections import deque
from concurrent.futures import ThreadPoolExecutor, Future
from tqdm.contrib.utils_worker import MonoWorker


def test_single_task_execution():
    """A single submitted task should run to completion."""
    worker = MonoWorker()
    result_container = []

    def task():
        time.sleep(0.05)
        result_container.append("done")

    future = worker.submit(task)
    assert isinstance(future, Future)
    # Wait for completion
    future.result(timeout=1)
    assert result_container == ["done"]
    assert future.done()
    assert not future.cancelled()


def test_waiting_task_replacement():
    """Submitting a second task should replace the waiting one if the first is still pending."""
    worker = MonoWorker()
    order = []

    def first_task():
        time.sleep(0.1)
        order.append("first")

    def second_task():
        order.append("second")

    # Submit first task; it will be waiting because the pool is busy
    first_future = worker.submit(first_task)
    # Immediately submit second task; it should replace the waiting first task
    second_future = worker.submit(second_task)

    # The first future should have been cancelled
    assert first_future.cancelled()
    # The second future should run
    second_future.result(timeout=1)
    assert order == ["second"]
    assert second_future.done()
    assert not second_future.cancelled()


def test_cancellation_of_waiting_task():
    """When a running task is still active, the waiting task should be cancelled upon a new submission."""
    worker = MonoWorker()
    order = []

    def long_task():
        time.sleep(0.2)
        order.append("long")

    def short_task():
        order.append("short")

    # Submit long task; it will be running
    long_future = worker.submit(long_task)
    # Submit short task; it will be waiting
    short_future = worker.submit(short_task)

    # Submit another task; this should cancel the waiting short_task
    worker.submit(lambda: order.append("new"))

    # Wait for long task to finish
    long_future.result(timeout=1)
    # The short task should have been cancelled
    assert short_future.cancelled()
    # The new task should have run
    assert order == ["long", "new"]
    assert long_future.done()
    assert not long_future.cancelled()

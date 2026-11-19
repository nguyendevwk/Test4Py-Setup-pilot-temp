import time
import pytest
from collections import deque
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from tqdm.contrib.utils_worker import MonoWorker


def test_single_task_execution():
    """A single submitted task should run to completion."""
    worker = MonoWorker()
    result_container = []

    def task():
        time.sleep(0.1)
        result_container.append("done")

    future = worker.submit(task)
    assert isinstance(future, type(worker.pool.submit(task)))
    # Wait for completion
    future.result(timeout=1)
    assert result_container == ["done"]


def test_waiting_task_replacement():
    """Submitting a new task while one is waiting should replace the waiting task."""
    worker = MonoWorker()
    order = []

    def first_task():
        time.sleep(0.2)
        order.append("first")

    def second_task():
        time.sleep(0.1)
        order.append("second")

    # Submit first task
    worker.submit(first_task)
    # Submit second task immediately; it should replace the waiting one
    worker.submit(second_task)

    # Wait for the running task to finish
    # The running task is the second_task because the first was replaced
    # The first task should never run
    # Since the pool has only one worker, the second_task will run immediately
    # and the first_task will be cancelled
    # Wait a bit longer than the longest task
    time.sleep(0.3)
    assert order == ["second"]


def test_cancellation_of_running_task():
    """If a running task is cancelled, it should not complete."""
    worker = MonoWorker()
    flag = {"ran": False}

    def long_task():
        # This task will be cancelled before it finishes
        for _ in range(5):
            time.sleep(0.1)
        flag["ran"] = True

    # Submit the long task
    future = worker.submit(long_task)
    # Immediately cancel the running task
    cancelled = future.cancel()
    # Since the task is already running, cancel() should return False
    assert cancelled is False
    # Wait to ensure the task would have finished if not cancelled
    time.sleep(0.6)
    assert flag["ran"] is False

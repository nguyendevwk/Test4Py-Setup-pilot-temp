import time
import pytest
from collections import deque
from concurrent.futures import ThreadPoolExecutor, Future
from tqdm.contrib.utils_worker import MonoWorker


def test_single_task_completion():
    """Submitting a single task should complete and be stored in the deque."""
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
    # The deque should contain the completed future
    assert len(worker.futures) == 1
    assert worker.futures[0].done()


def test_replacement_cancels_waiting():
    """Submitting a second task should cancel the waiting task and keep the running one."""
    worker = MonoWorker()
    order = []

    def long_task():
        order.append("start")
        time.sleep(0.2)
        order.append("end")

    def quick_task():
        order.append("quick")

    # Submit long task (will be running)
    long_future = worker.submit(long_task)
    # Submit quick task (should replace waiting)
    quick_future = worker.submit(quick_task)

    # The quick task should be cancelled before it starts
    assert quick_future.cancelled()
    # The long task should still be running
    assert not long_future.done()
    # Wait for long task to finish
    long_future.result(timeout=1)
    assert order == ["start", "end"]


def test_running_task_not_cancelled():
    """Ensure that a running task is never cancelled when a new task is submitted."""
    worker = MonoWorker()
    order = []

    def task_a():
        order.append("a_start")
        time.sleep(0.1)
        order.append("a_end")

    def task_b():
        order.append("b_start")
        time.sleep(0.05)
        order.append("b_end")

    # Submit first task
    future_a = worker.submit(task_a)
    # Immediately submit second task
    future_b = worker.submit(task_b)

    # The second task should be cancelled (waiting)
    assert future_b.cancelled()
    # The first task should complete
    future_a.result(timeout=1)
    assert order == ["a_start", "a_end"]

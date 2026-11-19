import time
import pytest
from concurrent.futures import Future
from tqdm.contrib.utils_worker import MonoWorker


def slow_task(duration, result):
    """Simulate a long running task."""
    time.sleep(duration)
    return result


def test_single_submission_and_completion():
    """Submitting one task should execute and return the result."""
    worker = MonoWorker()
    future = worker.submit(slow_task, 0.1, "ok")
    assert isinstance(future, Future)
    # Wait for completion
    result = future.result(timeout=1)
    assert result == "ok"
    # The future should be marked as done
    assert future.done()


def test_replacement_of_waiting_task():
    """Submitting a second task should cancel the previous waiting one."""
    worker = MonoWorker()
    # First task: long duration
    future1 = worker.submit(slow_task, 0.5, "first")
    # Second task: short duration, should replace the first
    future2 = worker.submit(slow_task, 0.1, "second")
    # The first future should be cancelled
    assert future1.cancelled() is True
    # The second future should complete with its result
    result = future2.result(timeout=1)
    assert result == "second"
    # Ensure the second future is done
    assert future2.done()


def test_running_task_is_not_canceled_and_waiting_is_cleared():
    """When a task is running, a new submission should cancel any waiting task but keep the running one."""
    worker = MonoWorker()
    # Submit a long task that will be running
    future_running = worker.submit(slow_task, 0.3, "running")
    # Submit a second task that will be waiting
    future_waiting = worker.submit(slow_task, 0.1, "waiting")
    # Submit a third task that should replace the waiting one
    future_new = worker.submit(slow_task, 0.1, "new")
    # The waiting task should be cancelled
    assert future_waiting.cancelled() is True
    # The running task should still be running
    assert future_running.done() is False
    # The new task should complete
    result = future_new.result(timeout=1)
    assert result == "new"
    # After the running task finishes, it should be done
    future_running.result(timeout=1)
    assert future_running.done() is True

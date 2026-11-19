import time
import pytest
from collections import deque
from concurrent.futures import ThreadPoolExecutor, Future
from tqdm.contrib.utils_worker import MonoWorker

def test_single_task_execution():
    """Submitting a single task should execute and complete."""
    worker = MonoWorker()
    result = []

    def task():
        time.sleep(0.05)
        result.append(42)

    future = worker.submit(task)
    assert isinstance(future, Future)
    # Wait for completion
    future.result(timeout=1)
    assert result == [42]
    # The future should be marked done
    assert future.done()

def test_waiting_task_replacement_and_cancellation():
    """Submitting a second task should replace the waiting one and cancel it."""
    worker = MonoWorker()
    executed = []

    def long_task():
        time.sleep(0.2)
        executed.append("long")

    def short_task():
        executed.append("short")

    # Submit long task first; it becomes waiting because no running task yet
    future1 = worker.submit(long_task)
    assert future1 is not None
    # Submit short task; it should replace the waiting long task
    future2 = worker.submit(short_task)
    assert future2 is not None
    # The long task should have been cancelled
    assert future1.cancelled()
    # The short task should run to completion
    future2.result(timeout=1)
    assert executed == ["short"]
    # No running task remains
    assert len(worker.futures) == 1
    assert worker.futures[0] is future2

def test_running_task_preserved_and_waiting_cleared():
    """When a task is running, a new submission should keep the running task and cancel any waiting."""
    worker = MonoWorker()
    order = []

    def running_task():
        order.append("run_start")
        time.sleep(0.15)
        order.append("run_end")

    def waiting_task():
        order.append("wait")

    # Submit running task
    future_run = worker.submit(running_task)
    # Submit waiting task; it should be queued
    future_wait = worker.submit(waiting_task)
    # Submit another waiting task; it should replace the previous waiting one
    future_wait2 = worker.submit(waiting_task)
    # The first waiting task should be cancelled
    assert future_wait.cancelled()
    # The second waiting task should be pending
    assert not future_wait2.done()
    # Wait for the running task to finish
    future_run.result(timeout=1)
    # After running task finishes, the waiting task should execute
    future_wait2.result(timeout=1)
    assert order == ["run_start", "run_end", "wait"]

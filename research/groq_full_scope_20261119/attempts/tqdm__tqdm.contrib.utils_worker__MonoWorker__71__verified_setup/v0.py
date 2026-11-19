import time
import pytest
from collections import deque
from concurrent.futures import Future
from tqdm.contrib.utils_worker import MonoWorker


def test_single_task_execution(tmp_path):
    """Submitting a single task should execute it and keep the future in the deque."""
    worker = MonoWorker()
    result_container = []

    def task():
        result_container.append("done")
        return 42

    future = worker.submit(task)
    # Wait for completion
    assert future.result(timeout=2) == 42
    assert result_container == ["done"]
    # The deque should contain exactly this future
    assert isinstance(worker.futures, deque)
    assert len(worker.futures) == 1
    assert worker.futures[0] is future
    assert future.done()


def test_replace_waiting_task(tmp_path):
    """Submitting a second task should replace the waiting task, not the running one."""
    worker = MonoWorker()
    call_order = []

    def first_task():
        call_order.append("first")
        time.sleep(0.1)
        return "first"

    def second_task():
        call_order.append("second")
        return "second"

    # Submit first task; it will start running
    future1 = worker.submit(first_task)
    # Submit second task; it should replace the waiting slot
    future2 = worker.submit(second_task)

    # The deque should contain both futures: running and waiting
    assert len(worker.futures) == 2
    # The first future should be the running one
    assert worker.futures[0] is future1
    # The second future should be the waiting one
    assert worker.futures[1] is future2

    # Wait for both to finish
    assert future1.result(timeout=2) == "first"
    assert future2.result(timeout=2) == "second"

    # Ensure the order of execution matches expectations
    assert call_order == ["first", "second"]


def test_cancellation_of_waiting_task(tmp_path):
    """When a new task is submitted while one is waiting, the waiting task should be cancelled."""
    worker = MonoWorker()
    call_log = []

    def long_task():
        call_log.append("long_start")
        time.sleep(0.5)
        call_log.append("long_end")
        return "long"

    def quick_task():
        call_log.append("quick")
        return "quick"

    # Submit a long task; it will be running
    future_long = worker.submit(long_task)
    # Submit a quick task; it should replace the waiting slot
    future_quick = worker.submit(quick_task)

    # The long task should still be running
    assert future_long.done() is False
    # The quick task should be waiting
    assert future_quick.done() is False

    # Wait for the quick task to finish
    assert future_quick.result(timeout=1) == "quick"

    # After quick task completes, the long task should still be running
    assert future_long.done() is False

    # Now cancel the long task manually to finish the test
    future_long.cancel()
    # The long task should be cancelled
    assert future_long.cancelled() is True
    # The call log should not contain "long_end" because it was cancelled
    assert "long_end" not in call_log
    # The call log should contain the start of the long task and the quick task
    assert call_log == ["long_start", "quick"]

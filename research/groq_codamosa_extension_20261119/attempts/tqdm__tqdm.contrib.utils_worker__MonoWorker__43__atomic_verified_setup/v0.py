import time
import pytest
from tqdm.contrib.utils_worker import MonoWorker
from concurrent.futures import Future


def test_single_task_execution(tmp_path):
    """Submitting one task should execute it and return a Future that completes."""
    worker = MonoWorker()
    result_container = []

    def task():
        result_container.append("done")

    future = worker.submit(task)
    assert isinstance(future, Future)
    # Wait for completion
    future.result(timeout=1)
    assert result_container == ["done"]
    assert future.done()


def test_waiting_task_replacement(tmp_path):
    """Submitting a second task replaces the waiting one when the queue is full."""
    worker = MonoWorker()
    order = []

    def first():
        order.append("first")
        time.sleep(0.2)  # keep it running

    def second():
        order.append("second")

    def third():
        order.append("third")

    # Submit first (running) and second (waiting)
    f1 = worker.submit(first)
    f2 = worker.submit(second)
    # Submit third, should cancel second
    f3 = worker.submit(third)

    # Wait for all to finish
    f1.result(timeout=1)
    f3.result(timeout=1)

    # second should never run
    assert order == ["first", "third"]
    assert f2.cancelled() or not f2.done()


def test_cancellation_of_waiting_task(tmp_path):
    """The waiting task should be cancelled when a new task is submitted."""
    worker = MonoWorker()
    executed = []

    def long_task():
        executed.append("long")
        time.sleep(0.5)

    def short_task():
        executed.append("short")

    # Submit long task (running) and short task (waiting)
    f_long = worker.submit(long_task)
    f_short = worker.submit(short_task)

    # Submit another task to trigger cancellation
    worker.submit(lambda: None)

    # Wait for long task to finish
    f_long.result(timeout=1)

    # short_task should have been cancelled
    assert f_short.cancelled()
    assert executed == ["long"]

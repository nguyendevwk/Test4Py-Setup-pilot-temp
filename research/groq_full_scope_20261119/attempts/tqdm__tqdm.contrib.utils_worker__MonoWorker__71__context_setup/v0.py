import time
import pytest
from collections import deque
from concurrent.futures import ThreadPoolExecutor, Future

from tqdm.contrib.utils_worker import MonoWorker


def test_single_submit_runs_and_returns_future():
    worker = MonoWorker()
    # A simple function that records its execution
    executed = []

    def task():
        executed.append("started")
        time.sleep(0.05)
        executed.append("finished")
        return 42

    future = worker.submit(task)
    assert isinstance(future, Future)
    # Wait for completion
    result = future.result(timeout=1)
    assert result == 42
    assert executed == ["started", "finished"]
    # The deque should contain only the running future
    assert len(worker.futures) == 1
    assert worker.futures[0] is future
    assert future.done()


def test_second_submit_replaces_waiting_and_cancels_previous_waiting():
    worker = MonoWorker()
    executed = []

    def long_task():
        executed.append("long_started")
        time.sleep(0.2)
        executed.append("long_finished")
        return "long"

    def short_task():
        executed.append("short_started")
        time.sleep(0.05)
        executed.append("short_finished")
        return "short"

    # Submit first long task
    long_future = worker.submit(long_task)
    # Immediately submit second short task, which should replace the waiting
    short_future = worker.submit(short_task)

    # The deque should contain the running long task and the waiting short task
    assert len(worker.futures) == 2
    assert worker.futures[0] is long_future
    assert worker.futures[1] is short_future

    # The short task should be cancelled before it starts
    assert short_future.cancelled() or short_future.done()
    # The long task should still be running
    assert not long_future.done()

    # Wait for the long task to finish
    long_result = long_future.result(timeout=1)
    assert long_result == "long"
    assert executed == ["long_started", "long_finished"]

    # Ensure the short task did not run
    assert "short_started" not in executed


def test_submit_more_than_two_tasks_keeps_only_running_and_last_waiting():
    worker = MonoWorker()
    executed = []

    def task_factory(name, delay):
        def task():
            executed.append(f"{name}_started")
            time.sleep(delay)
            executed.append(f"{name}_finished")
            return name
        return task

    # Submit three tasks in quick succession
    f1 = worker.submit(task_factory("first", 0.1))
    f2 = worker.submit(task_factory("second", 0.1))
    f3 = worker.submit(task_factory("third", 0.1))

    # The deque should contain the running first task and the waiting third task
    assert len(worker.futures) == 2
    assert worker.futures[0] is f1
    assert worker.futures[1] is f3

    # The second task should have been discarded and cancelled
    assert f2.cancelled() or f2.done()

    # Wait for the first task to finish
    assert f1.result(timeout=1) == "first"
    # The third task should still be pending
    assert not f3.done()

    # Now wait for the third task to finish
    assert f3.result(timeout=1) == "third"

    # Execution order should reflect that second task never ran
    assert executed == [
        "first_started",
        "first_finished",
        "third_started",
        "third_finished",
    ]

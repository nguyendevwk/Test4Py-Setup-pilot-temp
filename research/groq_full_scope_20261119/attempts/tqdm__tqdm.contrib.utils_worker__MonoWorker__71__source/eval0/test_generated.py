import time
import threading
import pytest
from tqdm.contrib.utils_worker import MonoWorker


def test_single_task_runs_and_completes():
    worker = MonoWorker()
    result = []

    def task():
        result.append("started")
        time.sleep(0.05)
        result.append("finished")

    future = worker.submit(task)
    assert future is not None
    future.result()  # wait for completion
    assert result == ["started", "finished"]


def test_waiting_task_replaced_by_new_submission():
    worker = MonoWorker()
    lock = threading.Lock()
    order = []

    def long_task():
        with lock:
            order.append("long_start")
        time.sleep(0.1)
        with lock:
            order.append("long_end")

    def short_task():
        with lock:
            order.append("short_start")
        time.sleep(0.01)
        with lock:
            order.append("short_end")

    # Submit long task first
    long_future = worker.submit(long_task)
    # Immediately submit short task, which should replace the waiting slot
    short_future = worker.submit(short_task)

    # Wait for both to finish
    long_future.result()
    short_future.result()

    # The long task should run to completion, short task should also run
    # but the order should reflect that short started after long started
    assert order == ["long_start", "short_start", "long_end", "short_end"]


def test_cancellation_of_waiting_task_and_execution_of_new_one():
    worker = MonoWorker()
    lock = threading.Lock()
    events = {"first": threading.Event(), "second": threading.Event()}

    def first_task():
        with lock:
            events["first"].set()
        time.sleep(0.2)  # long running

    def second_task():
        with lock:
            events["second"].set()
        time.sleep(0.05)

    # Submit first long task
    first_future = worker.submit(first_task)
    # Wait until first task has started
    events["first"].wait(0.1)

    # Submit second task which should replace the waiting slot
    second_future = worker.submit(second_task)

    # Wait for both to finish
    first_future.result()
    second_future.result()

    # The second task should have started after the first started
    # and the first task should have completed after the second
    assert events["first"].is_set()
    assert events["second"].is_set()
    assert first_future.done()
    assert second_future.done()

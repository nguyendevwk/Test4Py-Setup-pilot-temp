import time
import pytest
from collections import deque
from concurrent.futures import ThreadPoolExecutor, Future
from tqdm.contrib.utils_worker import MonoWorker


def test_single_task_execution():
    """Submitting a single task should execute it and return a Future."""
    worker = MonoWorker()

    def task():
        return 42

    future = worker.submit(task)
    assert isinstance(future, Future)
    assert future.done() is False  # not finished immediately
    result = future.result(timeout=1)
    assert result == 42
    # After completion, the deque should be empty
    assert len(worker.futures) == 0


def test_overwrite_waiting_task():
    """Submitting a second task while one is running should replace the waiting task."""
    worker = MonoWorker()

    # First task sleeps for a short time
    def long_task():
        time.sleep(0.2)
        return "long"

    # Second task is quick
    def short_task():
        return "short"

    # Submit first task
    long_future = worker.submit(long_task)
    # Submit second task immediately; it should replace the waiting slot
    short_future = worker.submit(short_task)

    # The long task should still be running
    assert long_future.done() is False
    # The short task should be waiting (not yet done)
    assert short_future.done() is False

    # Wait for the long task to finish
    long_result = long_future.result(timeout=1)
    assert long_result == "long"

    # After the long task finishes, the short task should start and finish
    short_result = short_future.result(timeout=1)
    assert short_result == "short"

    # Deque should be empty after both finish
    assert len(worker.futures) == 0


def test_submit_exception_handling(monkeypatch, capsys):
    """If the submitted function raises an exception during submission, it should be caught and printed."""
    worker = MonoWorker()

    # Monkeypatch the pool's submit to raise an exception
    def bad_submit(*args, **kwargs):
        raise RuntimeError("submission failed")

    monkeypatch.setattr(worker.pool, "submit", bad_submit)

    # Capture stdout to check error message
    with capsys.disabled():
        worker.submit(lambda: None)

    # Since submit failed, no future should be added
    assert len(worker.futures) == 0

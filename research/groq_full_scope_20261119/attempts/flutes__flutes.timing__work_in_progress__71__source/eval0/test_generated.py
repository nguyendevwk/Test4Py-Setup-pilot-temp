import time
import pytest
from flutes.timing import work_in_progress

def test_work_in_progress_context_prints_and_times(tmp_path, capsys):
    """Verify that the context manager prints the description and elapsed time."""
    start = time.time()
    with work_in_progress("Test block"):
        time.sleep(0.1)
    end = time.time()
    captured = capsys.readouterr()
    # The output should start with the description and end with "done."
    assert captured.out.startswith("Test block... ")
    assert captured.out.strip().endswith("done.")
    # The reported time should be close to the actual sleep duration
    reported_time = float(captured.out.split("(")[-1].rstrip("s)"))
    assert 0.09 <= reported_time <= 0.2
    # The real elapsed time should be at least as long as the reported time
    assert (end - start) >= reported_time

def test_work_in_progress_decorator_prints_and_times(capsys):
    """Verify that the decorator works and prints timing information."""
    @work_in_progress("Decorated function")
    def dummy():
        time.sleep(0.05)
    dummy()
    captured = capsys.readouterr()
    assert captured.out.startswith("Decorated function... ")
    assert captured.out.strip().endswith("done.")
    reported_time = float(captured.out.split("(")[-1].rstrip("s)"))
    assert 0.04 <= reported_time <= 0.1

def test_work_in_progress_exception_handling(capsys):
    """Verify that the context manager still prints timing when an exception occurs."""
    try:
        with work_in_progress("Error block"):
            raise ValueError("test error")
    except ValueError:
        pass
    captured = capsys.readouterr()
    assert captured.out.startswith("Error block... ")
    assert captured.out.strip().endswith("done.")
    reported_time = float(captured.out.split("(")[-1].rstrip("s)"))
    assert reported_time >= 0.0

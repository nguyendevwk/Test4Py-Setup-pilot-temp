import time
import builtins
import pytest
from flutes.timing import work_in_progress

def test_work_in_progress_prints_and_times(tmp_path, capsys):
    """Normal usage: context manager prints start and done with elapsed time."""
    start = time.time()
    with work_in_progress("Test task"):
        time.sleep(0.1)
    end = time.time()
    captured = capsys.readouterr()
    # Check that the start message is printed
    assert captured.out.startswith("Test task... ")
    # Check that the done message contains a time in seconds
    assert "done. (" in captured.out
    assert captured.out.endswith("s)\n")
    # Verify that the elapsed time reported is close to the actual sleep time
    reported_time = float(captured.out.split("(")[-1].rstrip("s)\n"))
    assert 0.09 <= reported_time <= 0.2
    # Ensure the overall duration is within expected bounds
    assert 0.09 <= (end - start) <= 0.3

def test_work_in_progress_zero_sleep(tmp_path, capsys):
    """Boundary case: zero sleep should still print a time close to zero."""
    with work_in_progress("Zero sleep"):
        pass
    captured = capsys.readouterr()
    assert captured.out.startswith("Zero sleep... ")
    assert captured.out.endswith("s)\n")
    reported_time = float(captured.out.split("(")[-1].rstrip("s)\n"))
    # The reported time should be very small
    assert reported_time < 0.01

def test_work_in_progress_exception_propagates_and_prints(tmp_path, capsys):
    """Error case: exception inside context should propagate and still print timing."""
    with pytest.raises(RuntimeError):
        with work_in_progress("Error task"):
            time.sleep(0.05)
            raise RuntimeError("boom")
    captured = capsys.readouterr()
    # Start message should be printed
    assert captured.out.startswith("Error task... ")
    # Done message should still appear even though exception was raised
    assert "done. (" in captured.out
    assert captured.out.endswith("s)\n")
    reported_time = float(captured.out.split("(")[-1].rstrip("s)\n"))
    # The reported time should be at least the sleep duration
    assert reported_time >= 0.04

import time
import pytest
from flutes.timing import work_in_progress

def test_work_in_progress_normal(capsys):
    """Verify that the context manager prints start and done messages
    and measures elapsed time for a normal block."""
    with work_in_progress("Test normal"):
        time.sleep(0.1)
    captured = capsys.readouterr()
    # The start message should be printed without a newline
    assert captured.out.startswith("Test normal... ")
    # The done message should contain the elapsed time in seconds
    assert "done. (" in captured.out
    # The elapsed time should be at least 0.1 seconds
    elapsed_str = captured.out.split("done. (")[1].rstrip("s)\n")
    elapsed = float(elapsed_str)
    assert elapsed >= 0.1

def test_work_in_progress_zero_sleep(capsys):
    """Boundary case: no sleep, elapsed time should be very small."""
    with work_in_progress("Zero sleep"):
        pass
    captured = capsys.readouterr()
    assert captured.out.startswith("Zero sleep... ")
    assert "done. (" in captured.out
    elapsed_str = captured.out.split("done. (")[1].rstrip("s)\n")
    elapsed = float(elapsed_str)
    # Allow a tiny amount of overhead
    assert elapsed < 0.01

def test_work_in_progress_exception(capsys):
    """Ensure that the done message is printed even if an exception occurs."""
    with pytest.raises(RuntimeError):
        with work_in_progress("Error case"):
            raise RuntimeError("boom")
    captured = capsys.readouterr()
    assert captured.out.startswith("Error case... ")
    assert "done. (" in captured.out
    # The elapsed time should still be present
    elapsed_str = captured.out.split("done. (")[1].rstrip("s)\n")
    float(elapsed_str)  # should not raise

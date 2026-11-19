import time
import pytest
from flutes.timing import work_in_progress


def test_work_in_progress_normal(capsys):
    """Verify that the context manager prints the start and end messages
    and measures a non‑negative duration."""
    with work_in_progress("Test task"):
        time.sleep(0.01)
    out, err = capsys.readouterr()
    # The output should contain the description, ellipsis, and the done message
    assert "Test task... " in out
    assert "done. (" in out
    # The duration should be at least 0.01 seconds
    duration_str = out.split("done. (")[1].rstrip("s)")
    duration = float(duration_str)
    assert duration >= 0.01


def test_work_in_progress_zero_sleep(capsys):
    """Boundary case: no sleep, duration should be very small but non‑negative."""
    with work_in_progress("Zero sleep"):
        pass
    out, err = capsys.readouterr()
    assert "Zero sleep... " in out
    assert "done. (" in out
    duration_str = out.split("done. (")[1].rstrip("s)")
    duration = float(duration_str)
    assert duration >= 0.0


def test_work_in_progress_exception(capsys):
    """If an exception occurs inside the block, the 'done' message should not be printed."""
    with pytest.raises(RuntimeError):
        with work_in_progress("Error task"):
            raise RuntimeError("boom")
    out, err = capsys.readouterr()
    # Only the start message should be present
    assert "Error task... " in out
    assert "done. (" not in out

import time
import builtins
import contextlib
import pytest
from flutes.timing import work_in_progress

def test_work_in_progress_with_sleep(capsys, tmp_path):
    """Verify that the context manager prints the description and elapsed time."""
    start = time.time()
    with work_in_progress("Sleeping"):
        time.sleep(0.1)
    end = time.time()
    captured = capsys.readouterr().out.strip()
    # The output should contain the description and the elapsed time in seconds.
    assert captured.startswith("Sleeping... done. (")
    # Extract the numeric part of the elapsed time.
    elapsed_str = captured.split("(")[-1].rstrip("s)")
    elapsed = float(elapsed_str)
    # The elapsed time should be at least the sleep duration and close to the real elapsed time.
    assert elapsed >= 0.1
    assert abs(elapsed - (end - start)) < 0.05

def test_work_in_progress_zero_sleep(capsys):
    """Test the boundary case where the block executes instantly."""
    with work_in_progress("Instant"):
        pass
    captured = capsys.readouterr().out.strip()
    assert captured.startswith("Instant... done. (")
    elapsed_str = captured.split("(")[-1].rstrip("s)")
    elapsed = float(elapsed_str)
    # The elapsed time should be very small.
    assert elapsed < 0.01

def test_work_in_progress_exception_propagates(capsys):
    """Ensure that an exception inside the block propagates and the message is still printed."""
    with pytest.raises(RuntimeError):
        with work_in_progress("Error"):
            raise RuntimeError("boom")
    captured = capsys.readouterr().out.strip()
    # The message should still be printed even though an exception occurred.
    assert captured.startswith("Error... done. (")
    elapsed_str = captured.split("(")[-1].rstrip("s)")
    elapsed = float(elapsed_str)
    assert elapsed < 0.01

import time
import pytest
from flutes.timing import work_in_progress

def test_work_in_progress_normal(tmp_path, capsys):
    """Verify normal execution prints start and end messages with elapsed time."""
    start = time.time()
    with work_in_progress("Test normal"):
        time.sleep(0.1)  # simulate work
    end = time.time()
    captured = capsys.readouterr()
    # Check that the start message is printed
    assert captured.out.startswith("Test normal... ")
    # Check that the end message contains "done." and a time in seconds
    assert "done. (" in captured.out
    assert captured.out.strip().endswith("s)")
    # Ensure the elapsed time reported is within reasonable bounds
    reported_time = float(captured.out.split("(")[-1].rstrip("s)"))
    assert 0.09 <= reported_time <= 0.5
    # Ensure the actual elapsed time matches the reported time within tolerance
    assert abs(reported_time - (end - start)) < 0.1

def test_work_in_progress_zero_sleep(tmp_path, capsys):
    """Boundary case: zero sleep should still report a small elapsed time."""
    with work_in_progress("Zero sleep"):
        pass  # no work
    captured = capsys.readouterr()
    assert captured.out.startswith("Zero sleep... ")
    assert "done. (" in captured.out
    reported_time = float(captured.out.split("(")[-1].rstrip("s)"))
    # The reported time should be very small but not negative
    assert reported_time >= 0.0
    assert reported_time < 0.1

def test_work_in_progress_exception(tmp_path, capsys):
    """Ensure that an exception inside the block still triggers the end message."""
    with pytest.raises(RuntimeError):
        with work_in_progress("Error test"):
            raise RuntimeError("boom")
    captured = capsys.readouterr()
    # The start message should be printed
    assert captured.out.startswith("Error test... ")
    # The end message should still appear even though an exception was raised
    assert "done. (" in captured.out
    assert captured.out.strip().endswith("s)")

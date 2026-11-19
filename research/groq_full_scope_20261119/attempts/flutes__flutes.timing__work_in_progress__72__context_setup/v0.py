import pytest
import time
from flutes.timing import work_in_progress

def test_work_in_progress_normal_block(capsys, tmp_path):
    """Verify that the context manager prints the description and elapsed time."""
    start = time.time()
    with work_in_progress("Test task"):
        time.sleep(0.1)
    end = time.time()
    captured = capsys.readouterr()
    # The output should start with the description and end with "done."
    assert captured.out.startswith("Test task... ")
    assert captured.out.strip().endswith("done.")
    # The elapsed time should be roughly the sleep duration
    elapsed_str = captured.out.split("done. (")[-1].rstrip(")")
    elapsed = float(elapsed_str.rstrip("s"))
    assert 0.09 <= elapsed <= 0.2
    # The total measured time should be close to the real elapsed time
    assert 0.09 <= (end - start) <= 0.2

def test_work_in_progress_zero_sleep(capsys):
    """Boundary case: no sleep, elapsed time should be very small."""
    with work_in_progress("Zero sleep"):
        pass
    captured = capsys.readouterr()
    assert captured.out.startswith("Zero sleep... ")
    assert captured.out.strip().endswith("done.")
    elapsed_str = captured.out.split("done. (")[-1].rstrip(")")
    elapsed = float(elapsed_str.rstrip("s"))
    # Expect elapsed time to be less than 0.01 seconds
    assert elapsed < 0.01

def test_work_in_progress_exception(capsys):
    """If an exception occurs inside the block, the context manager should not
    print the completion message."""
    with pytest.raises(RuntimeError):
        with work_in_progress("Error task"):
            raise RuntimeError("boom")
    captured = capsys.readouterr()
    # Only the description should be printed, no "done."
    assert captured.out.strip() == "Error task..."

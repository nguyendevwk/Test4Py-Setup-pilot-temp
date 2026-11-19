import pytest
import time
from flutes.timing import work_in_progress


def test_work_in_progress_normal(capsys, tmp_path):
    """Verify normal usage prints description and elapsed time."""
    start = time.time()
    with work_in_progress("Test task"):
        # Simulate a short operation
        time.sleep(0.1)
    end = time.time()
    captured = capsys.readouterr()
    # The output should start with the description and end with "done."
    assert captured.out.startswith("Test task... ")
    assert captured.out.strip().endswith("done.")
    # The elapsed time should be roughly the sleep duration
    elapsed_str = captured.out.strip().split("done. (")[1].rstrip("s)")
    elapsed = float(elapsed_str)
    assert 0.09 <= elapsed <= 0.2
    # Ensure the block actually took at least the sleep time
    assert end - start >= 0.09


def test_work_in_progress_zero_duration(capsys):
    """Verify that zero-duration blocks still print correctly."""
    with work_in_progress("Instant"):
        pass
    captured = capsys.readouterr()
    assert captured.out.startswith("Instant... ")
    assert captured.out.strip().endswith("done.")
    # elapsed time should be very small
    elapsed_str = captured.out.strip().split("done. (")[1].rstrip("s)")
    elapsed = float(elapsed_str)
    assert elapsed < 0.01


def test_work_in_progress_exception_propagation_and_logging(capsys):
    """Verify that an exception inside the block is re-raised and logging still occurs."""
    with pytest.raises(RuntimeError):
        with work_in_progress("Error task"):
            raise RuntimeError("boom")
    captured = capsys.readouterr()
    assert captured.out.startswith("Error task... ")
    assert captured.out.strip().endswith("done.")
    # Ensure the exception message is correct
    with pytest.raises(RuntimeError, match="boom"):
        with work_in_progress("Error task"):
            raise RuntimeError("boom")

import time
import pytest
from flutes.timing import work_in_progress


def test_work_in_progress_normal(capsys, tmp_path):
    """Verify normal execution prints description and elapsed time."""
    start = time.time()
    with work_in_progress("Test task"):
        time.sleep(0.1)
    end = time.time()
    captured = capsys.readouterr()
    # Check that the description and "done." are printed
    assert captured.out.startswith("Test task... ")
    assert "done." in captured.out
    # Extract the reported time from the output
    reported_time = float(captured.out.split("(")[-1].rstrip("s)\n"))
    # The reported time should be close to the actual elapsed time
    assert 0.09 <= reported_time <= 0.2
    # The actual elapsed time should also be within a reasonable range
    assert 0.09 <= (end - start) <= 0.2


def test_work_in_progress_default_description(capsys):
    """Verify that the default description is used when none is provided."""
    with work_in_progress():
        pass
    captured = capsys.readouterr()
    assert captured.out.startswith("Work in progress... ")
    assert "done." in captured.out


def test_work_in_progress_exception_handling(capsys):
    """Verify that an exception inside the context still triggers the final print."""
    with pytest.raises(RuntimeError):
        with work_in_progress("Error task"):
            raise RuntimeError("boom")
    captured = capsys.readouterr()
    # Even though an exception was raised, the final message should still be printed
    assert captured.out.startswith("Error task... ")
    assert "done." in captured.out
    # The reported time should be very small since the exception was immediate
    reported_time = float(captured.out.split("(")[-1].rstrip("s)\n"))
    assert reported_time < 0.01

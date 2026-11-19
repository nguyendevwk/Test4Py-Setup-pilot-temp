import time
import re
import pytest
from flutes.timing import work_in_progress

def test_work_in_progress_short_sleep(capsys):
    """Verify that the context manager prints the description and elapsed time."""
    with work_in_progress("Short sleep"):
        time.sleep(0.1)
    out, err = capsys.readouterr()
    assert out.startswith("Short sleep... ")
    assert "done. (" in out
    # Extract the time value and ensure it's at least 0.1s
    match = re.search(r"done\. \(([\d\.]+)s\)", out)
    assert match is not None, "Output did not contain elapsed time"
    elapsed = float(match.group(1))
    assert elapsed >= 0.1, f"Elapsed time {elapsed} is less than expected"

def test_work_in_progress_zero_sleep(capsys):
    """Boundary case: no sleep, elapsed time should be very small."""
    with work_in_progress("Zero sleep"):
        pass
    out, err = capsys.readouterr()
    assert out.startswith("Zero sleep... ")
    assert "done. (" in out
    match = re.search(r"done\. \(([\d\.]+)s\)", out)
    assert match is not None
    elapsed = float(match.group(1))
    # Allow a tiny amount of overhead
    assert elapsed < 0.05, f"Elapsed time {elapsed} is unexpectedly large"

def test_work_in_progress_exception_propagates_and_prints(capsys):
    """Ensure that an exception inside the context propagates and the
    completion message is still printed."""
    with pytest.raises(RuntimeError):
        with work_in_progress("Error test"):
            time.sleep(0.05)
            raise RuntimeError("boom")
    out, err = capsys.readouterr()
    assert out.startswith("Error test... ")
    assert "done. (" in out
    # Extract elapsed time and confirm it's at least 0.05s
    match = re.search(r"done\. \(([\d\.]+)s\)", out)
    assert match is not None
    elapsed = float(match.group(1))
    assert elapsed >= 0.05, f"Elapsed time {elapsed} is less than expected"

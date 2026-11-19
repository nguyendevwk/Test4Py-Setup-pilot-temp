import re
import time
import pytest
from flutes.timing import work_in_progress

def test_decorator_prints_and_returns_value(tmp_path, capsys):
    """Test that the decorator prints the description and returns the function result."""
    @work_in_progress("Test decorator")
    def add(a, b):
        return a + b

    result = add(2, 3)
    assert result == 5
    captured = capsys.readouterr()
    # The output should contain the description and the time in seconds
    assert captured.out.startswith("Test decorator... ")
    assert "done. (" in captured.out
    assert captured.out.strip().endswith("s)")

def test_context_manager_prints_and_handles_exception(tmp_path, capsys):
    """Test that the context manager prints the description and still prints on exception."""
    try:
        with work_in_progress("Test context"):
            time.sleep(0.01)
            raise ValueError("boom")
    except ValueError:
        pass
    captured = capsys.readouterr()
    # The output should contain the description and the time in seconds
    assert captured.out.startswith("Test context... ")
    assert "done. (" in captured.out
    assert captured.out.strip().endswith("s)")
    # Ensure the exception was propagated
    with pytest.raises(ValueError, match="boom"):
        with work_in_progress("Test context"):
            raise ValueError("boom")

def test_time_measurement_accuracy(tmp_path, capsys):
    """Test that the measured time is at least as long as the sleep duration."""
    sleep_duration = 0.05
    with work_in_progress("Sleep test"):
        time.sleep(sleep_duration)
    captured = capsys.readouterr()
    match = re.search(r"done\. \(([\d\.]+)s\)", captured.out)
    assert match is not None, "Output did not contain a time measurement"
    measured = float(match.group(1))
    # Allow a small margin for scheduling overhead
    assert measured >= sleep_duration * 0.9

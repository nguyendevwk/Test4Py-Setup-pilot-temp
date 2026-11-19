import sys
import time
import io
import contextlib
import pytest
from datetime import datetime

# Import the target context manager
from thefuck.logs import debug_time

# Helper to capture debug output
@contextlib.contextmanager
def capture_stdout():
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        yield sys.stdout
    finally:
        sys.stdout = old_stdout

def test_debug_time_normal_execution():
    """The context manager should log the elapsed time for normal execution."""
    with capture_stdout() as out:
        with debug_time("normal test"):
            # Simulate some work
            time.sleep(0.01)
    output = out.getvalue()
    assert "normal test took:" in output
    # Ensure the elapsed time is a positive number
    elapsed_str = output.split("normal test took:")[1].strip()
    # The format is a timedelta string, e.g., "0:00:00.010123"
    # Convert to float seconds for a simple check
    elapsed_seconds = float(elapsed_str.split(":")[-1])
    assert elapsed_seconds >= 0.0

def test_debug_time_exception_propagation():
    """An exception inside the context should propagate and still log the elapsed time."""
    with capture_stdout() as out:
        with pytest.raises(RuntimeError):
            with debug_time("exception test"):
                time.sleep(0.005)
                raise RuntimeError("boom")
    output = out.getvalue()
    assert "exception test took:" in output
    # The elapsed time should be at least the sleep duration
    elapsed_str = output.split("exception test took:")[1].strip()
    elapsed_seconds = float(elapsed_str.split(":")[-1])
    assert elapsed_seconds >= 0.005

def test_debug_time_boundary_zero_sleep():
    """When no work is done, the elapsed time should be very small but non-negative."""
    with capture_stdout() as out:
        with debug_time("zero sleep"):
            pass
    output = out.getvalue()
    assert "zero sleep took:" in output
    elapsed_str = output.split("zero sleep took:")[1].strip()
    elapsed_seconds = float(elapsed_str.split(":")[-1])
    assert elapsed_seconds >= 0.0

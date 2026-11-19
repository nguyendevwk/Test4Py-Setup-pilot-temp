import importlib
import time
import types
import pytest

# Import the target module
from thefuck.logs import debug_time

# Helper to capture debug calls
def capture_debug():
    calls = []

    def fake_debug(msg):
        calls.append(msg)

    return fake_debug, calls


def test_debug_time_measures_elapsed(tmp_path):
    """Normal usage: debug_time should record elapsed time."""
    fake_debug, calls = capture_debug()
    # Monkey‑patch the module's debug function
    import thefuck.logs
    thefuck.logs.debug = fake_debug

    with debug_time("test_message"):
        time.sleep(0.01)

    assert len(calls) == 1
    msg = calls[0]
    assert msg.startswith("test_message took: ")
    # The elapsed time should be at least 0.01 seconds
    elapsed_str = msg.split("took: ")[1]
    elapsed = float(elapsed_str.split()[0])
    assert elapsed >= 0.009  # allow small overhead


def test_debug_time_zero_sleep(tmp_path):
    """Boundary case: no sleep, elapsed time should be very small."""
    fake_debug, calls = capture_debug()
    import thefuck.logs
    thefuck.logs.debug = fake_debug

    with debug_time("zero_sleep"):
        pass  # no delay

    assert len(calls) == 1
    msg = calls[0]
    assert msg.startswith("zero_sleep took: ")
    elapsed_str = msg.split("took: ")[1]
    elapsed = float(elapsed_str.split()[0])
    assert elapsed < 0.001  # should be almost instantaneous


def test_debug_time_exception_propagates_and_logs(tmp_path):
    """Error behavior: exception inside context should propagate and still log."""
    fake_debug, calls = capture_debug()
    import thefuck.logs
    thefuck.logs.debug = fake_debug

    with pytest.raises(RuntimeError):
        with debug_time("error_case"):
            raise RuntimeError("boom")

    assert len(calls) == 1
    msg = calls[0]
    assert msg.startswith("error_case took: ")
    # Ensure the exception message propagates
    with pytest.raises(RuntimeError, match="boom"):
        with debug_time("error_case"):
            raise RuntimeError("boom")

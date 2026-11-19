import builtins
import importlib
import types
import sys
import time
import pytest

# Import the target module
from thefuck import logs

# Helper to capture calls to logs.debug
class DebugRecorder:
    def __init__(self):
        self.calls = []

    def __call__(self, msg):
        self.calls.append(msg)

def test_debug_time_basic_yield_and_logging(monkeypatch):
    """
    Verify that debug_time yields control and logs the elapsed time.
    """
    recorder = DebugRecorder()
    monkeypatch.setattr(logs, "debug", recorder)

    # Use the context manager
    with logs.debug_time("test operation") as ctx:
        # Inside the context, ctx should be None
        assert ctx is None
        # Simulate some work
        time.sleep(0.01)

    # After exiting, debug should have been called once
    assert len(recorder.calls) == 1
    # The message should contain the provided msg and a duration string
    assert recorder.calls[0].startswith("test operation took:")

def test_debug_time_boundary_zero_duration(monkeypatch):
    """
    Test that the context manager works even when the block executes instantly.
    """
    recorder = DebugRecorder()
    monkeypatch.setattr(logs, "debug", recorder)

    with logs.debug_time("instant"):
        pass  # no work

    assert len(recorder.calls) == 1
    # Duration should be very small but still a string
    assert "instant took:" in recorder.calls[0]
    # Ensure the duration part is a valid time delta representation
    duration_part = recorder.calls[0].split("instant took:")[1].strip()
    # It should end with a unit like 'seconds' or similar
    assert any(unit in duration_part for unit in ("seconds", "microseconds", "milliseconds"))

def test_debug_time_exception_propagation(monkeypatch):
    """
    Ensure that an exception inside the context propagates and debug is still called.
    """
    recorder = DebugRecorder()
    monkeypatch.setattr(logs, "debug", recorder)

    with pytest.raises(RuntimeError):
        with logs.debug_time("error case"):
            raise RuntimeError("boom")

    # Even though an exception was raised, debug should still have been called
    assert len(recorder.calls) == 1
    assert recorder.calls[0].startswith("error case took:")

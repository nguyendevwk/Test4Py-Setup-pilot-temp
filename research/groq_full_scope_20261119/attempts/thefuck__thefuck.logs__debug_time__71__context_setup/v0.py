import builtins
import sys
import types
import pytest
from datetime import datetime, timedelta

# Import the target module
import thefuck.logs as logs

# Helper to patch datetime.now in the logs module
class DummyDateTime:
    def __init__(self, start, end):
        self._start = start
        self._end = end
        self._called = 0

    def now(self):
        if self._called == 0:
            self._called += 1
            return self._start
        else:
            return self._end

def test_debug_time_debug_enabled(monkeypatch, capsys):
    """When settings.debug is True, debug_time should write a debug message to stderr."""
    # Enable debug
    monkeypatch.setattr(logs.settings, "debug", True)
    # Capture stderr
    with logs.debug_time("test_msg"):
        pass
    out, err = capsys.readouterr()
    assert "DEBUG:" in err
    assert "test_msg took:" in err

def test_debug_time_debug_disabled(monkeypatch, capsys):
    """When settings.debug is False, debug_time should not write anything to stderr."""
    # Disable debug
    monkeypatch.setattr(logs.settings, "debug", False)
    with logs.debug_time("no_output"):
        pass
    out, err = capsys.readouterr()
    assert err == ""

def test_debug_time_duration(monkeypatch, capsys):
    """debug_time should report the correct duration between start and end times."""
    # Enable debug
    monkeypatch.setattr(logs.settings, "debug", True)
    # Set fixed start and end times
    start = datetime(2023, 1, 1, 12, 0, 0)
    end = start + timedelta(seconds=2, milliseconds=500)
    dummy = DummyDateTime(start, end)
    monkeypatch.setattr(logs, "datetime", dummy)
    with logs.debug_time("duration_test"):
        pass
    out, err = capsys.readouterr()
    # The duration should be approximately 2.5 seconds
    assert "2.5" in err or "2.500" in err or "2.50" in err

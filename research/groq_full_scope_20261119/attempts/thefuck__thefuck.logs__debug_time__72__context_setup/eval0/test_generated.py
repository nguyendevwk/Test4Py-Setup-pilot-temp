import sys
import io
import types
import pytest
from contextlib import contextmanager
from datetime import datetime
from thefuck.logs import debug_time, debug, color
from thefuck.conf import settings

# Helper to temporarily set settings attributes
@pytest.fixture
def set_debug(monkeypatch):
    def _set(value):
        monkeypatch.setattr(settings, "debug", value)
    return _set

@pytest.fixture
def set_no_colors(monkeypatch):
    def _set(value):
        monkeypatch.setattr(settings, "no_colors", value)
    return _set

def test_debug_time_calls_debug_on_success(set_debug, capsys):
    """When the context completes normally, debug_time should call debug with elapsed time."""
    set_debug(True)
    with debug_time("test_msg") as ctx:
        # perform trivial work
        x = 1 + 1
    # Capture stderr output
    captured = capsys.readouterr()
    # The output should contain the message and a time delta
    assert "test_msg took:" in captured.err
    # Ensure the output is not empty
    assert captured.err.strip() != ""

def test_debug_time_calls_debug_on_exception(set_debug, capsys):
    """If an exception occurs inside the context, debug_time should still call debug."""
    set_debug(True)
    with pytest.raises(RuntimeError):
        with debug_time("error_msg"):
            raise RuntimeError("boom")
    captured = capsys.readouterr()
    assert "error_msg took:" in captured.err
    assert captured.err.strip() != ""

def test_debug_time_no_output_when_debug_disabled(set_debug, capsys):
    """When settings.debug is False, debug_time should not produce any output."""
    set_debug(False)
    with debug_time("silent_msg"):
        pass
    captured = capsys.readouterr()
    assert captured.err == ""

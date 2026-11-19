import sys
import builtins
import importlib
import types
import pytest
from contextlib import redirect_stderr
from io import StringIO

# Import the target module
from thefuck.logs import debug
from thefuck import conf

# Helper to temporarily set settings.debug
@pytest.fixture
def set_debug(monkeypatch):
    def _set(value):
        monkeypatch.setattr(conf.settings, "debug", value)
    return _set

def test_debug_writes_to_stderr_when_enabled(set_debug, capsys):
    """When settings.debug is True, debug() writes a formatted message to stderr."""
    set_debug(True)
    debug("test message")
    captured = capsys.readouterr()
    # The output should contain the word DEBUG and the message
    assert "DEBUG:" in captured.err
    assert "test message" in captured.err
    # Ensure no output to stdout
    assert captured.out == ""

def test_debug_does_not_write_when_disabled(set_debug, capsys):
    """When settings.debug is False, debug() produces no output."""
    set_debug(False)
    debug("should not appear")
    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == ""

def test_debug_handles_non_string_input(set_debug, capsys):
    """debug() should convert non-string messages to string without raising."""
    set_debug(True)
    debug(12345)  # integer input
    captured = capsys.readouterr()
    # The output should contain the string representation of the integer
    assert "12345" in captured.err
    assert "DEBUG:" in captured.err

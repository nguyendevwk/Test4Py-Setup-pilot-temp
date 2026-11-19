import sys
import io
import contextlib
import importlib

import pytest

# Import the module under test
from thefuck.logs import debug
from thefuck.conf import settings


@contextlib.contextmanager
def toggle_debug(value):
    """Temporarily set settings.debug to `value` and restore it afterwards."""
    original = settings.debug
    settings.debug = value
    try:
        yield
    finally:
        settings.debug = original


def test_debug_writes_formatted_message(capsys):
    """When debug mode is enabled, debug() writes a formatted message to stderr."""
    test_msg = "Test message"
    with toggle_debug(True):
        debug(test_msg)
    captured = capsys.readouterr()
    # The output should contain the message and the ANSI reset code
    assert test_msg in captured.err
    assert "\x1b[0m" in captured.err  # reset code from colorama
    # Ensure the output ends with a newline
    assert captured.err.endswith("\n")


def test_debug_handles_empty_message(capsys):
    """debug() should handle an empty string without raising an exception."""
    with toggle_debug(True):
        debug("")
    captured = capsys.readouterr()
    # The output should still contain the DEBUG prefix and a newline
    assert captured.err.startswith("\x1b[34m\x1b[1mDEBUG:\x1b[0m ")
    assert captured.err.endswith("\n")
    # No message content after the prefix
    assert captured.err.strip().endswith("DEBUG:")


def test_debug_no_output_when_disabled(capsys):
    """When debug mode is disabled, debug() should not write anything to stderr."""
    with toggle_debug(False):
        debug("Should not appear")
    captured = capsys.readouterr()
    assert captured.err == ""

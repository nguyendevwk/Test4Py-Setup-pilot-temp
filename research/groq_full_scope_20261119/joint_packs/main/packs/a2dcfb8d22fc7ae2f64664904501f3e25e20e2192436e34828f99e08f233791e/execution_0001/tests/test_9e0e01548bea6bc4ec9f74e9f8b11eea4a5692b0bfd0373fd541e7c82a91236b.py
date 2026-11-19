import sys
import io
import types
import importlib
import contextlib

import pytest

# Import the target module
from thefuck import logs
from thefuck.conf import settings

# Helper to capture stderr
@contextlib.contextmanager
def capture_stderr():
    old_stderr = sys.stderr
    sys.stderr = io.StringIO()
    try:
        yield sys.stderr
    finally:
        sys.stderr = old_stderr

def test_debug_outputs_formatted_message_when_enabled():
    """When settings.debug is True, debug writes a formatted message to stderr."""
    settings.debug = True
    settings.no_colors = False
    msg = "test message"

    with capture_stderr() as err:
        logs.debug(msg)

    output = err.getvalue()
    # The output should contain the message and color codes
    assert "DEBUG:" in output
    assert msg in output
    # Color codes are present because no_colors is False
    assert "\x1b[34m" in output  # blue
    assert "\x1b[1m" in output   # bold

def test_debug_suppresses_output_when_disabled():
    """When settings.debug is False, debug writes nothing to stderr."""
    settings.debug = False
    settings.no_colors = False
    msg = "should not appear"

    with capture_stderr() as err:
        logs.debug(msg)

    assert err.getvalue() == ""

def test_debug_without_colors_when_no_colors_enabled():
    """When settings.no_colors is True, debug writes message without color codes."""
    settings.debug = True
    settings.no_colors = True
    msg = "no colors"

    with capture_stderr() as err:
        logs.debug(msg)

    output = err.getvalue()
    # No ANSI escape sequences should be present
    assert "\x1b[" not in output
    assert "DEBUG:" in output
    assert msg in output

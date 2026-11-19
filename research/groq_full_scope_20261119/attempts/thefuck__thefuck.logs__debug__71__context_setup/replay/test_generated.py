import sys
import io
import pytest
from thefuck.logs import debug, color
from thefuck.conf import settings

@pytest.fixture(autouse=True)
def reset_settings():
    """Ensure settings are reset after each test."""
    original_debug = settings.debug
    original_no_colors = settings.no_colors
    yield
    settings.debug = original_debug
    settings.no_colors = original_no_colors

def test_debug_writes_to_stderr_when_enabled(tmp_path):
    """When settings.debug is True, debug() writes a formatted message to stderr."""
    settings.debug = True
    captured = io.StringIO()
    original_stderr = sys.stderr
    sys.stderr = captured
    try:
        debug("Test message")
    finally:
        sys.stderr = original_stderr
    output = captured.getvalue()
    # The output should contain the message and the ANSI codes for blue and bold
    assert "Test message" in output
    assert "\x1b[34m" in output  # blue
    assert "\x1b[1m" in output   # bold

def test_debug_does_not_write_when_disabled(tmp_path):
    """When settings.debug is False, debug() writes nothing to stderr."""
    settings.debug = False
    captured = io.StringIO()
    original_stderr = sys.stderr
    sys.stderr = captured
    try:
        debug("Should not appear")
    finally:
        sys.stderr = original_stderr
    assert captured.getvalue() == ""

def test_color_returns_empty_when_no_colors(tmp_path):
    """color() returns an empty string when settings.no_colors is True."""
    settings.no_colors = True
    assert color("\x1b[31m") == ""
    # When colors are enabled, it should return the original string
    settings.no_colors = False
    assert color("\x1b[31m") == "\x1b[31m"

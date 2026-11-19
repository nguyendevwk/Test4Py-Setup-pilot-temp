import sys
import io
import pytest
from thefuck.logs import warn

def capture_stderr(func, *args, **kwargs):
    """Execute func and capture its output to sys.stderr."""
    old_stderr = sys.stderr
    sys.stderr = io.StringIO()
    try:
        func(*args, **kwargs)
        return sys.stderr.getvalue()
    finally:
        sys.stderr = old_stderr

def test_warn_outputs_expected_format():
    """Warn should write a line prefixed with the warning marker and reset."""
    output = capture_stderr(warn, "Test warning")
    # The output should end with a newline and contain the title.
    assert output.endswith("\n")
    assert "Test warning" in output
    # The warning marker should start with a color code (non‑empty).
    assert output.startswith("\x1b[")

def test_warn_handles_empty_title():
    """Warn should still output a line even if the title is empty."""
    output = capture_stderr(warn, "")
    # Should still produce a line with just the warning marker and reset.
    assert output.endswith("\n")
    # No title text should appear between markers.
    assert output.strip() == "\x1b[0m" or output.strip().startswith("\x1b[")

def test_warn_preserves_special_characters():
    """Warn should not alter special characters in the title."""
    special = "⚡🚀🔥"
    output = capture_stderr(warn, special)
    # The special characters should be present verbatim in the output.
    assert special in output
    # The output should still end with a newline.
    assert output.endswith("\n")

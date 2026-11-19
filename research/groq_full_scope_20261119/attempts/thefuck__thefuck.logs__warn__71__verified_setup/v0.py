import sys
import io
import pytest
import colorama
from thefuck.logs import warn

# Ensure colorama is initialized so that color codes are produced
colorama.init(autoreset=True)

def capture_stderr(func, *args, **kwargs):
    """Utility to capture stderr output of a function call."""
    old_stderr = sys.stderr
    sys.stderr = io.StringIO()
    try:
        func(*args, **kwargs)
        return sys.stderr.getvalue()
    finally:
        sys.stderr = old_stderr

def test_warn_normal_title():
    """Warn should write a formatted warning with a normal title."""
    output = capture_stderr(warn, "Test warning")
    # The output should contain the title and the ANSI reset code
    assert "Test warning" in output
    # It should start with the warning prefix and end with a newline
    assert output.startswith("\x1b[41;37;1m[WARN] ")
    assert output.endswith("\x1b[0m\n")

def test_warn_empty_title():
    """Warn should handle an empty title gracefully."""
    output = capture_stderr(warn, "")
    # The output should still contain the warning prefix and reset code
    assert output.startswith("\x1b[41;37;1m[WARN] ")
    assert output.endswith("\x1b[0m\n")
    # No title text should appear between the brackets
    assert output == "\x1b[41;37;1m[WARN] \x1b[0m\n"

def test_warn_special_characters():
    """Warn should correctly escape special characters in the title."""
    special_title = "Line1\nLine2\t✓"
    output = capture_stderr(warn, special_title)
    # The output should contain the literal special characters
    assert "Line1\nLine2\t✓" in output
    # Ensure the formatting is still correct
    assert output.startswith("\x1b[41;37;1m[WARN] ")
    assert output.endswith("\x1b[0m\n")

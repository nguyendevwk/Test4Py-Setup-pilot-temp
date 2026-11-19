import sys
import io
import pytest
from thefuck.logs import warn
from thefuck.conf import settings

def test_warn_normal_output(capsys):
    """Warn should write a formatted warning to stderr with color codes."""
    warn("Test warning")
    captured = capsys.readouterr()
    # The output should end with a newline and contain the title
    assert captured.err.endswith("\n")
    assert "Test warning" in captured.err
    # When colors are enabled, the output should contain ANSI escape sequences
    assert "\x1b[" in captured.err

def test_warn_empty_title(capsys):
    """Warn should handle an empty title without raising."""
    warn("")
    captured = capsys.readouterr()
    # The output should still contain the warning prefix and a newline
    assert captured.err.startswith("\x1b[")  # color prefix
    assert captured.err.strip().endswith("[WARN]")  # no title after
    assert captured.err.endswith("\n")

def test_warn_non_string_raises():
    """Passing a non-string title should raise a TypeError."""
    with pytest.raises(TypeError):
        warn(None)

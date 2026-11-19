import sys
import io
import pytest
from thefuck.logs import version

def capture_stderr(func, *args, **kwargs):
    """Utility to capture sys.stderr output of a function call."""
    old_stderr = sys.stderr
    sys.stderr = io.StringIO()
    try:
        func(*args, **kwargs)
        return sys.stderr.getvalue()
    finally:
        sys.stderr = old_stderr

def test_version_normal_output():
    """Test that version writes the expected formatted string."""
    output = capture_stderr(version, "1.2.3", "3.8.5", "bash")
    expected = "The Fuck 1.2.3 using Python 3.8.5 and bash\n"
    assert output == expected

def test_version_with_empty_strings():
    """Test that empty strings are handled gracefully."""
    output = capture_stderr(version, "", "", "")
    expected = "The Fuck  using Python  and \n"
    assert output == expected

def test_version_with_special_characters():
    """Test that special characters in arguments are preserved."""
    output = capture_stderr(version, "v1.0\n", "3.9.1\r", "zsh\t")
    expected = "The Fuck v1.0\n using Python 3.9.1\r and zsh\t\n"
    assert output == expected

import sys
import io
import pytest
from thefuck.logs import version

def capture_stderr(func, *args, **kwargs):
    """Helper to capture stderr output of a function call."""
    old_stderr = sys.stderr
    sys.stderr = io.StringIO()
    try:
        func(*args, **kwargs)
        return sys.stderr.getvalue()
    finally:
        sys.stderr = old_stderr

def test_version_normal_output():
    """Verify that version writes the expected string for typical inputs."""
    output = capture_stderr(version, "1.2.3", "3.10.5", "bash")
    expected = "The Fuck 1.2.3 using Python 3.10.5 and bash\n"
    assert output == expected

def test_version_empty_strings():
    """Check behavior when empty strings are provided for all parameters."""
    output = capture_stderr(version, "", "", "")
    expected = "The Fuck  using Python  and \n"
    assert output == expected

def test_version_non_string_inputs():
    """Ensure that non-string inputs are converted to strings correctly."""
    output = capture_stderr(version, 42, 3.8, ["zsh"])
    expected = "The Fuck 42 using Python 3.8 and ['zsh']\n"
    assert output == expected

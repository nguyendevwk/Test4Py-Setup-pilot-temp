import sys
import io
import pytest
from thefuck.logs import version

def test_version_outputs_expected_string():
    """The function should write the correct formatted string to stderr."""
    # Arrange
    buf = io.StringIO()
    original_stderr = sys.stderr
    sys.stderr = buf
    try:
        # Act
        version("2.0.0", "3.11.2", "bash")
        # Assert
        output = buf.getvalue()
        assert output == "The Fuck 2.0.0 using Python 3.11.2 and bash\n"
    finally:
        sys.stderr = original_stderr

def test_version_handles_empty_strings():
    """Empty input strings should still produce a valid output line."""
    buf = io.StringIO()
    original_stderr = sys.stderr
    sys.stderr = buf
    try:
        version("", "", "")
        output = buf.getvalue()
        assert output == "The Fuck  using Python  and \n"
    finally:
        sys.stderr = original_stderr

def test_version_returns_none_and_does_not_raise():
    """The function should return None and not raise an exception for any input."""
    # Using a variety of inputs to ensure no exceptions are raised
    inputs = [
        ("1.0", "2.7", "zsh"),
        ("", "3.9", "fish"),
        ("v1", "", "powershell"),
        ("", "", ""),
    ]
    for thefuck_version, python_version, shell_info in inputs:
        try:
            result = version(thefuck_version, python_version, shell_info)
            assert result is None
        except Exception as exc:
            pytest.fail(f"version raised an exception {exc!r} for inputs {thefuck_version!r}, {python_version!r}, {shell_info!r}")

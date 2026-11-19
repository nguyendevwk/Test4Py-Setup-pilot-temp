import sys
import io
import pytest
from thefuck.logs import version

def test_version_outputs_expected_string():
    """The function should write the correct formatted string to stderr."""
    # Arrange
    fake_stderr = io.StringIO()
    original_stderr = sys.stderr
    sys.stderr = fake_stderr

    # Act
    version("2.0.0", "3.11.2", "bash")

    # Assert
    output = fake_stderr.getvalue()
    assert output == "The Fuck 2.0.0 using Python 3.11.2 and bash\n"

    # Cleanup
    sys.stderr = original_stderr

def test_version_handles_empty_strings():
    """The function should handle empty string arguments gracefully."""
    # Arrange
    fake_stderr = io.StringIO()
    original_stderr = sys.stderr
    sys.stderr = fake_stderr

    # Act
    version("", "", "")

    # Assert
    output = fake_stderr.getvalue()
    assert output == "The Fuck  using Python  and \n"

    # Cleanup
    sys.stderr = original_stderr

def test_version_does_not_raise_on_unicode_input():
    """The function should not raise an exception when given unicode strings."""
    # Arrange
    fake_stderr = io.StringIO()
    original_stderr = sys.stderr
    sys.stderr = fake_stderr

    # Act & Assert
    try:
        version("v1.0‑β", "3.9‑α", "zsh")
    except Exception as exc:
        pytest.fail(f"version raised an exception with unicode input: {exc}")

    # Verify output
    output = fake_stderr.getvalue()
    assert output == "The Fuck v1.0‑β using Python 3.9‑α and zsh\n"

    # Cleanup
    sys.stderr = original_stderr

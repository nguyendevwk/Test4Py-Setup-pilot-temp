import sys
import io
import pytest
from thefuck.logs import failed

def test_failed_writes_colored_message_to_stderr(tmp_path):
    """The function should write the message wrapped in ANSI color codes to stderr."""
    # Capture stderr
    old_stderr = sys.stderr
    sys.stderr = io.StringIO()
    try:
        failed("Error occurred")
        output = sys.stderr.getvalue()
    finally:
        sys.stderr = old_stderr

    # The output should contain the message, a newline, and ANSI reset code
    assert "Error occurred" in output
    assert output.endswith("\n")
    # ANSI reset code is \x1b[0m
    assert "\x1b[0m" in output
    # ANSI red code is \x1b[31m
    assert "\x1b[31m" in output

def test_failed_with_empty_string(tmp_path):
    """An empty message should still produce a newline and reset code."""
    old_stderr = sys.stderr
    sys.stderr = io.StringIO()
    try:
        failed("")
        output = sys.stderr.getvalue()
    finally:
        sys.stderr = old_stderr

    assert output == "\x1b[31m\x1b[0m\n" or output == "\x1b[31m\x1b[0m\n"

def test_failed_with_non_string_raises_type_error():
    """Passing a non-string should raise a TypeError due to string formatting."""
    with pytest.raises(TypeError):
        failed(None)

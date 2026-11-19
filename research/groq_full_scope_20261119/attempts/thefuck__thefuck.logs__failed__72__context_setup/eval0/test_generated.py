import sys
import io
import pytest
from thefuck import logs
from thefuck.conf import settings

@pytest.fixture
def capture_stderr():
    """Capture writes to sys.stderr."""
    original = sys.stderr
    buffer = io.StringIO()
    sys.stderr = buffer
    try:
        yield buffer
    finally:
        sys.stderr = original

def test_failed_with_string_message(capture_stderr):
    """`failed` writes the message with color codes when colors are enabled."""
    # Ensure colors are enabled
    settings.no_colors = False
    logs.failed("Test message")
    output = capture_stderr.getvalue()
    # The output should contain the message and reset code
    assert "Test message" in output
    assert output.endswith("\n")
    # Color codes should be present
    assert "\x1b[31m" in output  # RED
    assert "\x1b[0m" in output   # RESET

def test_failed_with_non_string_message(capture_stderr):
    """`failed` accepts non‑string arguments and converts them to string."""
    settings.no_colors = False
    logs.failed(42)
    output = capture_stderr.getvalue()
    # The numeric value should be converted to string
    assert "42" in output
    assert output.endswith("\n")

def test_failed_without_colors(capture_stderr):
    """When `no_colors` is True, no color codes are written."""
    settings.no_colors = True
    logs.failed("No color")
    output = capture_stderr.getvalue()
    # No ANSI escape sequences should be present
    assert "\x1b[" not in output
    assert "No color" in output
    assert output.endswith("\n")

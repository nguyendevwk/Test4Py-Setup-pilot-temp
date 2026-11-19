import sys
import builtins
import importlib
import types
import pytest

# Import the target module
from thefuck.logs import warn, color
from thefuck import conf

# Helper to capture stderr
@pytest.fixture
def capture_stderr():
    def _capture():
        from io import StringIO
        old_stderr = sys.stderr
        sys.stderr = StringIO()
        try:
            yield sys.stderr
        finally:
            sys.stderr = old_stderr
    return _capture

def test_warn_with_colors(capture_stderr):
    """Warn should output colored warning when colors are enabled."""
    # Ensure colors are enabled
    conf.settings.no_colors = False
    with capture_stderr() as err:
        warn("Test warning")
    output = err.getvalue()
    # The output should contain the warning prefix and the title
    assert "[WARN] Test warning" in output
    # It should include ANSI escape codes for red background and white text
    assert "\x1b[41m\x1b[37m\x1b[1m" in output  # Back.RED + Fore.WHITE + Style.BRIGHT
    # Reset code should appear at the end
    assert "\x1b[0m" in output

def test_warn_no_colors(capture_stderr):
    """Warn should output plain text when colors are disabled."""
    # Disable colors
    conf.settings.no_colors = True
    with capture_stderr() as err:
        warn("No color warning")
    output = err.getvalue()
    # No ANSI codes should be present
    assert "\x1b[" not in output
    assert "[WARN] No color warning" in output

def test_warn_empty_title(capture_stderr):
    """Warn should handle an empty title gracefully."""
    conf.settings.no_colors = False
    with capture_stderr() as err:
        warn("")
    output = err.getvalue()
    # The warning prefix should still appear
    assert "[WARN] " in output
    # No title text should follow the colon
    assert output.strip().endswith("[WARN]") or output.strip().endswith("[WARN] ")

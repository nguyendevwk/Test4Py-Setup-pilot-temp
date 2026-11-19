import builtins
import io
import sys
import types
import pytest
from thefuck.logs import configured_successfully, color
from thefuck import conf

# Helper to capture stdout
@pytest.fixture
def capture_stdout():
    def _capture(func, *args, **kwargs):
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            func(*args, **kwargs)
            return sys.stdout.getvalue()
        finally:
            sys.stdout = old_stdout
    return _capture

def test_configured_successfully_default_colors(capture_stdout):
    # Ensure default color output when no_colors is False
    conf.settings.no_colors = False
    class DummyConf:
        reload = "source ~/.bashrc"
    output = capture_stdout(configured_successfully, DummyConf())
    # The output should contain the reload command and color codes
    assert "source ~/.bashrc" in output
    assert "\x1b[1m" in output  # bright style code
    assert "\x1b[0m" in output  # reset code

def test_configured_successfully_no_colors(capture_stdout):
    # When colors are disabled, the output should not contain ANSI codes
    conf.settings.no_colors = True
    class DummyConf:
        reload = "exec $SHELL"
    output = capture_stdout(configured_successfully, DummyConf())
    # No ANSI escape sequences should be present
    assert "\x1b[" not in output
    assert "exec $SHELL" in output

def test_configured_successfully_empty_reload(capture_stdout):
    # Test boundary case where reload string is empty
    conf.settings.no_colors = False
    class DummyConf:
        reload = ""
    output = capture_stdout(configured_successfully, DummyConf())
    # The output should still contain the reload placeholder but be empty
    assert "reload" in output  # placeholder text
    # Ensure no trailing spaces or unexpected characters
    assert output.strip().endswith("or restart your shell.")

import builtins
import io
import sys
import types

import pytest

# Import the target function and its dependencies
from thefuck.logs import configured_successfully, color
from thefuck import conf

# Helper to capture stdout
@pytest.fixture
def capture_stdout():
    original_stdout = sys.stdout
    stream = io.StringIO()
    sys.stdout = stream
    yield stream
    sys.stdout = original_stdout

# Test normal behavior with colors enabled
def test_configured_successfully_with_colors(capture_stdout):
    # Create a simple object with a reload attribute
    class DummyConfig:
        reload = "source ~/.thefuck"
    config = DummyConfig()
    # Ensure colors are enabled
    conf.settings.no_colors = False
    configured_successfully(config)
    output = capture_stdout.getvalue()
    # The output should contain the reload string and color codes
    assert "source ~/.thefuck" in output
    assert "\x1b[1m" in output  # bright style code
    assert "\x1b[0m" in output  # reset code

# Test behavior when colors are disabled
def test_configured_successfully_no_colors(capture_stdout):
    class DummyConfig:
        reload = "source ~/.thefuck"
    config = DummyConfig()
    # Disable colors
    conf.settings.no_colors = True
    configured_successfully(config)
    output = capture_stdout.getvalue()
    # No color codes should be present
    assert "\x1b[1m" not in output
    assert "\x1b[0m" not in output
    # The reload string should still be present
    assert "source ~/.thefuck" in output

# Test that missing reload attribute raises AttributeError
def test_configured_successfully_missing_reload():
    class DummyConfig:
        pass  # no reload attribute
    config = DummyConfig()
    with pytest.raises(AttributeError):
        configured_successfully(config)

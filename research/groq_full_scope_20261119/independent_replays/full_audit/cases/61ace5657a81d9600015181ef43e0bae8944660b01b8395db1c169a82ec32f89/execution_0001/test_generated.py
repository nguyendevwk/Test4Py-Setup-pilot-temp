import builtins
import types
import pytest
from contextlib import redirect_stdout
from io import StringIO

# Import the target function
from thefuck.logs import configured_successfully

# Helper to create a simple object with a `reload` attribute
class DummyConfig:
    def __init__(self, reload):
        self.reload = reload

def test_configured_successfully_prints_expected_output(capsys):
    """Verify that the function prints the correct message with a given reload command."""
    config = DummyConfig(reload="source ~/.bashrc")
    configured_successfully(config)
    captured = capsys.readouterr()
    expected_substring = "alias configured successfully!"
    assert expected_substring in captured.out
    assert "source ~/.bashrc" in captured.out
    # Ensure the message ends with a period
    assert captured.out.strip().endswith("shell.")

def test_configured_successfully_handles_empty_reload(capsys):
    """Boundary case: reload attribute is an empty string."""
    config = DummyConfig(reload="")
    configured_successfully(config)
    captured = capsys.readouterr()
    # The reload placeholder should be empty but the rest of the message remains
    assert "alias configured successfully!" in captured.out
    assert "or restart your shell." in captured.out
    # No stray spaces where reload would be
    assert "  or restart" not in captured.out

def test_configured_successfully_raises_attribute_error_on_missing_reload():
    """Error case: configuration object lacks a 'reload' attribute."""
    # Create an object without a reload attribute
    config = types.SimpleNamespace()
    with pytest.raises(AttributeError):
        configured_successfully(config)

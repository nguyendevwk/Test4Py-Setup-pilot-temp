import builtins
import sys
import types
import pytest
from thefuck.logs import configured_successfully

class DummyReload:
    def __init__(self, value):
        self.reload = value

def test_configured_successfully_prints_expected_output(capsys):
    """Verify that the function prints the correct success message."""
    details = DummyReload("source ~/.bashrc")
    configured_successfully(details)
    captured = capsys.readouterr()
    # The message should contain the words 'fuck', 'configured successfully', and the reload command.
    assert "fuck" in captured.out
    assert "configured successfully" in captured.out
    assert "source ~/.bashrc" in captured.out
    # Ensure the message ends with a newline.
    assert captured.out.endswith("\n")

def test_configured_successfully_handles_empty_reload(capsys):
    """Verify that an empty reload string is still printed correctly."""
    details = DummyReload("")
    configured_successfully(details)
    captured = capsys.readouterr()
    # The reload part should be empty but the rest of the message remains.
    assert "fuck" in captured.out
    assert "configured successfully" in captured.out
    assert "source" not in captured.out  # No reload command present

def test_configured_successfully_raises_attribute_error_on_missing_reload():
    """Verify that an AttributeError is raised if the details object lacks a 'reload' attribute."""
    class BadDetails:
        pass
    with pytest.raises(AttributeError):
        configured_successfully(BadDetails())

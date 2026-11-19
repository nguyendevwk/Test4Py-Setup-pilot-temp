import sys
import io
import pytest
from contextlib import redirect_stderr

# Import the target function and related modules
from thefuck.logs import confirm_text
from thefuck.conf import settings
from thefuck import const

# Helper class to simulate a corrected command object
class DummyCommand:
    def __init__(self, script, side_effect=False):
        self.script = script
        self.side_effect = side_effect

def test_confirm_text_no_side_effect(monkeypatch):
    # Disable colors for deterministic output
    monkeypatch.setattr(settings, "no_colors", True)

    cmd = DummyCommand("echo hello")
    buf = io.StringIO()
    with redirect_stderr(buf):
        confirm_text(cmd)
    output = buf.getvalue()

    # Expected prefix and command
    expected_prefix = const.USER_COMMAND_MARK
    assert expected_prefix in output
    assert "echo hello" in output
    # No side effect marker
    assert "(+side effect)" not in output
    # Ensure the prompt markers are present
    assert "[enter/↑/↓/ctrl+c]" in output

def test_confirm_text_with_side_effect(monkeypatch):
    # Disable colors for deterministic output
    monkeypatch.setattr(settings, "no_colors", True)

    cmd = DummyCommand("rm -rf /", side_effect=True)
    buf = io.StringIO()
    with redirect_stderr(buf):
        confirm_text(cmd)
    output = buf.getvalue()

    # Expected prefix and command
    expected_prefix = const.USER_COMMAND_MARK
    assert expected_prefix in output
    assert "rm -rf /" in output
    # Side effect marker should be present
    assert "(+side effect)" in output
    # Ensure the prompt markers are present
    assert "[enter/↑/↓/ctrl+c]" in output

def test_confirm_text_invalid_command():
    # Pass an object missing required attributes to trigger AttributeError
    class BadCommand:
        pass

    bad_cmd = BadCommand()
    with pytest.raises(AttributeError):
        confirm_text(bad_cmd)

import sys
import io
import pytest
from contextlib import redirect_stderr

# Import the function under test
from thefuck.logs import show_corrected_command
# Import the settings object to manipulate the no_colors flag
from thefuck.conf import settings

# Helper class to mimic the corrected_command object
class DummyCommand:
    def __init__(self, script, side_effect=False):
        self.script = script
        self.side_effect = side_effect

def capture_stderr(func, *args, **kwargs):
    """Utility to capture stderr output of a function call."""
    buf = io.StringIO()
    with redirect_stderr(buf):
        func(*args, **kwargs)
    return buf.getvalue()

def test_show_corrected_command_no_side_effect_and_colors_enabled():
    """Test normal output when side effect is False and colors are enabled."""
    # Ensure colors are enabled
    settings.no_colors = False
    cmd = DummyCommand("echo hello")
    output = capture_stderr(show_corrected_command, cmd)
    # The output should contain the script and no side effect marker
    assert "echo hello" in output
    assert "(+side effect)" not in output
    # The output should start with the USER_COMMAND_MARK constant
    from thefuck.const import USER_COMMAND_MARK
    assert output.startswith(USER_COMMAND_MARK)
    # The output should end with a newline
    assert output.endswith("\n")

def test_show_corrected_command_with_side_effect_and_colors_enabled():
    """Test output when side effect is True and colors are enabled."""
    settings.no_colors = False
    cmd = DummyCommand("ls -l", side_effect=True)
    output = capture_stderr(show_corrected_command, cmd)
    # The output should contain the side effect marker
    assert "(+side effect)" in output
    # The script should still be present
    assert "ls -l" in output
    # Ensure the marker is correctly formatted
    assert output.strip().endswith("(+side effect)")

def test_show_corrected_command_no_colors():
    """Test output when colors are disabled (no_colors=True)."""
    settings.no_colors = True
    cmd = DummyCommand("git status")
    output = capture_stderr(show_corrected_command, cmd)
    # When colors are disabled, no ANSI codes should appear
    # The output should not contain any escape sequences (e.g., \x1b)
    assert "\x1b" not in output
    # The script should still be present
    assert "git status" in output
    # The output should still end with a newline
    assert output.endswith("\n")

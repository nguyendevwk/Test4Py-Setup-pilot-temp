import sys
import io
import colorama
import pytest

# Import the target function and constants
from thefuck.logs import show_corrected_command
from thefuck import const

# Ensure colorama is initialized so that color codes are produced
colorama.init(autoreset=True)


class DummyCommand:
    """Simple command object with script and side_effect attributes."""
    def __init__(self, script, side_effect=False):
        self.script = script
        self.side_effect = side_effect


def capture_stderr(func, *args, **kwargs):
    """Utility to capture stderr output of a function call."""
    old_stderr = sys.stderr
    sys.stderr = io.StringIO()
    try:
        func(*args, **kwargs)
        return sys.stderr.getvalue()
    finally:
        sys.stderr = old_stderr


def test_show_corrected_command_with_side_effect():
    """Command with a side effect should append the side effect marker."""
    cmd = DummyCommand("echo hello", side_effect=True)
    output = capture_stderr(show_corrected_command, cmd)
    # The output should start with the user command mark
    assert output.startswith(const.USER_COMMAND_MARK)
    # The script should be present
    assert "echo hello" in output
    # The side effect marker should be present
    assert "(+side effect)" in output
    # The output should end with a newline
    assert output.endswith("\n")


def test_show_corrected_command_without_side_effect():
    """Command without a side effect should not append the side effect marker."""
    cmd = DummyCommand("ls -l", side_effect=False)
    output = capture_stderr(show_corrected_command, cmd)
    assert output.startswith(const.USER_COMMAND_MARK)
    assert "ls -l" in output
    # No side effect marker
    assert "(+side effect)" not in output
    assert output.endswith("\n")


def test_show_corrected_command_with_unicode_script():
    """Command script containing Unicode characters should be handled correctly."""
    cmd = DummyCommand("echo 你好", side_effect=True)
    output = capture_stderr(show_corrected_command, cmd)
    assert output.startswith(const.USER_COMMAND_MARK)
    assert "echo 你好" in output
    assert "(+side effect)" in output
    assert output.endswith("\n")

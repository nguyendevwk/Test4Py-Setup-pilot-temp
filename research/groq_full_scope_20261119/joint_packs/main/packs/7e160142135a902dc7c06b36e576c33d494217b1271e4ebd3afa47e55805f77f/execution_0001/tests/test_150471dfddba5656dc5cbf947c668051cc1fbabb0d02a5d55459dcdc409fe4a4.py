import sys
import io
import pytest
from thefuck.logs import show_corrected_command
from thefuck.const import USER_COMMAND_MARK

class DummyCommand:
    def __init__(self, script, side_effect=False):
        self.script = script
        self.side_effect = side_effect

def capture_stderr(func, *args, **kwargs):
    """Utility to capture stderr output of a function."""
    old_stderr = sys.stderr
    sys.stderr = io.StringIO()
    try:
        func(*args, **kwargs)
        return sys.stderr.getvalue()
    finally:
        sys.stderr = old_stderr

def test_show_corrected_command_with_side_effect():
    cmd = DummyCommand("echo hello", side_effect=True)
    output = capture_stderr(show_corrected_command, cmd)
    expected_prefix = USER_COMMAND_MARK
    assert output.startswith(expected_prefix)
    assert "echo hello" in output
    assert "(+side effect)" in output
    assert output.endswith("\n")

def test_show_corrected_command_without_side_effect():
    cmd = DummyCommand("ls -l", side_effect=False)
    output = capture_stderr(show_corrected_command, cmd)
    expected_prefix = USER_COMMAND_MARK
    assert output.startswith(expected_prefix)
    assert "ls -l" in output
    assert "(+side effect)" not in output
    assert output.endswith("\n")

def test_show_corrected_command_special_characters():
    cmd = DummyCommand("grep 'pattern' file.txt", side_effect=False)
    output = capture_stderr(show_corrected_command, cmd)
    assert USER_COMMAND_MARK in output
    assert "grep 'pattern' file.txt" in output
    assert "(+side effect)" not in output
    assert output.endswith("\n")

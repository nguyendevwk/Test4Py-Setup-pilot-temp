import sys
import io
import pytest
from thefuck.logs import confirm_text
from thefuck import const

class DummyCommand:
    def __init__(self, script, side_effect=False):
        self.script = script
        self.side_effect = side_effect

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

def test_confirm_text_basic(capture_stderr):
    cmd = DummyCommand("echo hello")
    confirm_text(cmd)
    output = capture_stderr.getvalue()
    # Basic components
    assert const.USER_COMMAND_MARK in output
    assert "echo hello" in output
    assert "[\x1b[32menter\x1b[0m/\x1b[34m↑\x1b[0m/\x1b[34m↓\x1b[0m/\x1b[31mctrl+c\x1b[0m]" in output
    # No side effect marker
    assert "(+side effect)" not in output

def test_confirm_text_with_side_effect(capture_stderr):
    cmd = DummyCommand("ls -l", side_effect=True)
    confirm_text(cmd)
    output = capture_stderr.getvalue()
    # Side effect marker present
    assert "(+side effect)" in output
    # Ensure script still present
    assert "ls -l" in output

def test_confirm_text_empty_script(capture_stderr):
    cmd = DummyCommand("")
    confirm_text(cmd)
    output = capture_stderr.getvalue()
    # Even with empty script, markers should still appear
    assert const.USER_COMMAND_MARK in output
    assert "[\x1b[32menter\x1b[0m/\x1b[34m↑\x1b[0m/\x1b[34m↓\x1b[0m/\x1b[31mctrl+c\x1b[0m]" in output
    # No script text
    assert "script" not in output

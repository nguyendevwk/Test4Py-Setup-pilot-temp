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

def test_confirm_text_without_side_effect(capture_stderr):
    cmd = DummyCommand("echo hello")
    confirm_text(cmd)
    output = capture_stderr.getvalue()
    # The output should contain the command script and no side effect marker
    assert "echo hello" in output
    assert "(+side effect)" not in output
    # It should start with the user command mark
    assert output.startswith(const.USER_COMMAND_MARK)
    # It should contain the prompt markers
    assert "[enter/↑/↓/ctrl+c]" in output

def test_confirm_text_with_side_effect(capture_stderr):
    cmd = DummyCommand("rm -rf /", side_effect=True)
    confirm_text(cmd)
    output = capture_stderr.getvalue()
    # The side effect marker should be present
    assert "(+side effect)" in output
    # The command script should still be present
    assert "rm -rf /" in output

def test_confirm_text_output_formatting(capture_stderr):
    cmd = DummyCommand("ls -la")
    confirm_text(cmd)
    output = capture_stderr.getvalue()
    # The output should contain ANSI escape codes for bold and colors
    # Check for presence of at least one escape code sequence
    assert "\033[" in output
    # Ensure that the reset code appears after the command
    reset_code = "\033[0m"
    assert reset_code in output
    # The output should not contain any raw colorama constants
    assert "colorama" not in output

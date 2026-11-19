import sys
import io
import pytest
from thefuck.logs import confirm_text
from thefuck import const

# Helper to capture stderr output
@pytest.fixture
def capture_stderr():
    original_stderr = sys.stderr
    buffer = io.StringIO()
    sys.stderr = buffer
    try:
        yield buffer
    finally:
        sys.stderr = original_stderr

# Simple object mimicking a corrected command
class DummyCommand:
    def __init__(self, script, side_effect=False):
        self.script = script
        self.side_effect = side_effect

def test_confirm_text_basic(capture_stderr):
    cmd = DummyCommand("echo hello")
    confirm_text(cmd)
    output = capture_stderr.getvalue()
    # Basic components should be present
    assert const.USER_COMMAND_MARK in output
    assert "echo hello" in output
    assert "[enter/↑/↓/ctrl+c]" in output
    # No side effect marker
    assert "(+side effect)" not in output

def test_confirm_text_with_side_effect(capture_stderr):
    cmd = DummyCommand("rm -rf /", side_effect=True)
    confirm_text(cmd)
    output = capture_stderr.getvalue()
    # Side effect marker should appear
    assert "(+side effect)" in output
    # Ensure script is still present
    assert "rm -rf /" in output

def test_confirm_text_invalid_command_raises_attribute_error(capture_stderr):
    # Pass an object missing required attributes
    class BadCommand:
        pass
    bad_cmd = BadCommand()
    with pytest.raises(AttributeError):
        confirm_text(bad_cmd)

import sys
import io
import pytest
from thefuck.logs import confirm_text
from thefuck import const

# Helper to capture stderr output
@pytest.fixture
def captured_stderr():
    original_stderr = sys.stderr
    buffer = io.StringIO()
    sys.stderr = buffer
    try:
        yield buffer
    finally:
        sys.stderr = original_stderr

def test_confirm_text_basic(captured_stderr):
    class Cmd:
        script = "ls -la"
        side_effect = False
    confirm_text(Cmd())
    output = captured_stderr.getvalue()
    # Should contain the user command mark and the script
    assert const.USER_COMMAND_MARK in output
    assert "ls -la" in output
    # Should not contain side effect marker
    assert "(+side effect)" not in output
    # Should contain the prompt symbols
    assert "[enter/↑/↓/ctrl+c]" in output

def test_confirm_text_with_side_effect(captured_stderr):
    class Cmd:
        script = "git commit"
        side_effect = True
    confirm_text(Cmd())
    output = captured_stderr.getvalue()
    # Should contain the side effect marker
    assert "(+side effect)" in output
    # Should still contain the script
    assert "git commit" in output

def test_confirm_text_empty_script(captured_stderr):
    class Cmd:
        script = ""
        side_effect = False
    confirm_text(Cmd())
    output = captured_stderr.getvalue()
    # Should still write something to stderr
    assert output != ""
    # Should not raise errors even with empty script
    assert const.USER_COMMAND_MARK in output

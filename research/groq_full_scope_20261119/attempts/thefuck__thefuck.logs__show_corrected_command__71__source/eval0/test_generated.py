import sys
import io
import pytest
from thefuck.logs import show_corrected_command
from thefuck import const

# Helper to capture stderr output
@pytest.fixture
def captured_stderr():
    old_stderr = sys.stderr
    sys.stderr = io.StringIO()
    try:
        yield sys.stderr
    finally:
        sys.stderr = old_stderr

def test_show_corrected_command_with_side_effect(captured_stderr):
    class Cmd:
        script = "git commit -m 'msg'"
        side_effect = True
    show_corrected_command(Cmd)
    output = captured_stderr.getvalue()
    assert const.USER_COMMAND_MARK in output
    assert "git commit -m 'msg'" in output
    assert "(+side effect)" in output
    # Ensure formatting includes color codes
    assert "\x1b[" in output

def test_show_corrected_command_without_side_effect(captured_stderr):
    class Cmd:
        script = "ls -la"
        side_effect = False
    show_corrected_command(Cmd)
    output = captured_stderr.getvalue()
    assert const.USER_COMMAND_MARK in output
    assert "ls -la" in output
    assert "(+side effect)" not in output
    assert "\x1b[" in output

def test_show_corrected_command_empty_script(captured_stderr):
    class Cmd:
        script = ""
        side_effect = False
    show_corrected_command(Cmd)
    output = captured_stderr.getvalue()
    assert const.USER_COMMAND_MARK in output
    assert output.endswith("\n")
    # Even with empty script, side effect string should be absent
    assert "(+side effect)" not in output

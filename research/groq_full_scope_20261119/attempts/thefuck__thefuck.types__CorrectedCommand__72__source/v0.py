import sys
import os
import io
import pytest
from thefuck.types import CorrectedCommand
from thefuck import settings
from thefuck import shell

# Helper to capture stdout
@pytest.fixture
def captured_stdout(monkeypatch):
    stream = io.StringIO()
    monkeypatch.setattr(sys, "stdout", stream)
    return stream

def test_equality_and_hash(monkeypatch):
    # Create two commands with same script and side_effect but different priority
    def dummy_side_effect(cmd, script): pass
    cmd1 = CorrectedCommand("ls", dummy_side_effect, priority=10)
    cmd2 = CorrectedCommand("ls", dummy_side_effect, priority=20)
    # Equality ignores priority
    assert cmd1 == cmd2
    # Hash also ignores priority
    assert hash(cmd1) == hash(cmd2)
    # Representation includes priority
    assert "priority=10" in repr(cmd1)
    assert "priority=20" in repr(cmd2)

def test_get_script_with_repeat(monkeypatch):
    # Enable repeat and debug
    monkeypatch.setattr(settings, "repeat", True)
    monkeypatch.setattr(settings, "debug", True)
    # Dummy side_effect
    def dummy_side_effect(cmd, script): pass
    cmd = CorrectedCommand("echo hello", dummy_side_effect, priority=5)
    # Expected repeat command
    repeat_cmd = f"{shell.quote('echo hello')} --repeat --debug {shell.quote('echo hello')}"
    expected = shell.or_("echo hello", repeat_cmd)
    assert cmd._get_script() == expected

def test_run_writes_script_and_history(monkeypatch, captured_stdout):
    # Disable repeat and history alteration
    monkeypatch.setattr(settings, "repeat", False)
    monkeypatch.setattr(settings, "alter_history", False)
    # Track side_effect call
    called = {"called": False}
    def dummy_side_effect(cmd, script):
        called["called"] = True
    cmd = CorrectedCommand("pwd", dummy_side_effect, priority=1)
    # Dummy old_cmd
    class DummyCmd: pass
    old_cmd = DummyCmd()
    # Run command
    cmd.run(old_cmd)
    # Side effect should have been called
    assert called["called"] is True
    # Script should be written to stdout
    assert captured_stdout.getvalue() == "pwd"
    # History should not be modified
    # (We cannot easily check history, but alter_history flag is False)

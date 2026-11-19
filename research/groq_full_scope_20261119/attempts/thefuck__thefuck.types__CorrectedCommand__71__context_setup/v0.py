import sys
import os
import io
import pytest
from thefuck.types import CorrectedCommand
from thefuck import conf, logs, shells

# Helper to capture stdout
@pytest.fixture
def capture_stdout():
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    yield sys.stdout
    sys.stdout = old_stdout

def test_equality_and_hash(monkeypatch):
    # Create two commands with same script and side_effect but different priority
    cmd1 = CorrectedCommand("echo hi", None, 10)
    cmd2 = CorrectedCommand("echo hi", None, 20)
    # They should be equal ignoring priority
    assert cmd1 == cmd2
    # Hash should also be equal
    assert hash(cmd1) == hash(cmd2)
    # Changing script should break equality
    cmd3 = CorrectedCommand("echo bye", None, 10)
    assert cmd1 != cmd3

def test_run_writes_script_and_history(monkeypatch, capture_stdout):
    # Prepare a side_effect that records its call
    side_effect_called = {"called": False}
    def side_effect(old_cmd, script):
        side_effect_called["called"] = True
    # Patch settings to disable history alteration
    monkeypatch.setattr(conf.settings, "alter_history", False)
    # Patch shell.put_to_history to raise if called
    monkeypatch.setattr(shells.shell, "put_to_history", lambda x: (_ for _ in ()).throw(RuntimeError("should not be called")))
    # Create command and run
    cmd = CorrectedCommand("ls -l", side_effect, 5)
    cmd.run(None)
    # Verify side_effect was called
    assert side_effect_called["called"] is True
    # Verify script was written to stdout
    assert capture_stdout.getvalue() == "ls -l"

def test_get_script_with_repeat(monkeypatch):
    # Patch settings.repeat and debug
    monkeypatch.setattr(conf.settings, "repeat", True)
    monkeypatch.setattr(conf.settings, "debug", False)
    # Patch get_alias to return a fake alias
    monkeypatch.setattr("thefuck.utils.get_alias", lambda: "thefuck")
    # Patch shell.quote to return quoted script
    monkeypatch.setattr(shells.shell, "quote", lambda s: f"'{s}'")
    # Patch shell.or_ to concatenate with "||"
    monkeypatch.setattr(shells.shell, "or_", lambda a, b: f"{a} || {b}")
    cmd = CorrectedCommand("echo test", None, 1)
    expected_repeat = "echo test || thefuck --repeat  --force-command 'echo test'"
    assert cmd._get_script() == expected_repeat
    # Now disable repeat
    monkeypatch.setattr(conf.settings, "repeat", False)
    assert cmd._get_script() == "echo test"

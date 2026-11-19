import io
import os
import sys
import types
import pytest

# Import the target class
from thefuck.types import CorrectedCommand
# Import settings and shell for monkeypatching
from thefuck import settings, shell
from thefuck import logs

# Helper to capture stdout
@pytest.fixture
def captured_stdout():
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    yield sys.stdout
    sys.stdout = old_stdout

# 1. Test equality and hashing ignore priority
def test_eq_and_hash_ignore_priority():
    cmd1 = CorrectedCommand("ls", None, 10)
    cmd2 = CorrectedCommand("ls", None, 20)
    assert cmd1 == cmd2
    assert hash(cmd1) == hash(cmd2)

    # Different script
    cmd3 = CorrectedCommand("pwd", None, 10)
    assert cmd1 != cmd3

    # Different side_effect
    def side_effect1(old_cmd, script): pass
    def side_effect2(old_cmd, script): pass
    cmd4 = CorrectedCommand("ls", side_effect1, 10)
    cmd5 = CorrectedCommand("ls", side_effect2, 10)
    assert cmd4 != cmd5

# 2. Test run writes script to stdout and records history
def test_run_writes_stdout_and_history(monkeypatch, captured_stdout):
    # Prepare a dummy side_effect that records its call
    called = {}
    def dummy_side_effect(old_cmd, script):
        called['old_cmd'] = old_cmd
        called['script'] = script

    # Monkeypatch settings to disable repeat and history alteration
    monkeypatch.setattr(settings, "repeat", False)
    monkeypatch.setattr(settings, "alter_history", True)
    monkeypatch.setattr(settings, "debug", False)

    # Capture history writes
    history_calls = []
    def fake_put_to_history(cmd):
        history_calls.append(cmd)
    monkeypatch.setattr(shell, "put_to_history", fake_put_to_history)

    # Create command and run
    corr = CorrectedCommand("echo hello", dummy_side_effect, 5)
    old_cmd = types.SimpleNamespace(command="wrong")
    corr.run(old_cmd)

    # Assert side_effect called correctly
    assert called['old_cmd'] is old_cmd
    assert called['script'] == "echo hello"

    # Assert stdout contains the script
    assert captured_stdout.getvalue() == "echo hello"

    # Assert history was updated
    assert history_calls == ["echo hello"]

# 3. Test _get_script with repeat enabled
def test_get_script_repeat(monkeypatch):
    # Enable repeat and debug
    monkeypatch.setattr(settings, "repeat", True)
    monkeypatch.setattr(settings, "debug", True)

    # Mock get_alias to return a fake alias
    monkeypatch.setattr("thefuck.types.get_alias", lambda: "thefuck")

    # Mock shell.quote to return quoted script
    monkeypatch.setattr(shell, "quote", lambda s: f"'{s}'")

    # Mock shell.or_ to concatenate with "||"
    monkeypatch.setattr(shell, "or_", lambda a, b: f"{a} || {b}")

    # Create command
    corr = CorrectedCommand("ls -l", None, 1)

    # Expected repeat command
    repeat_fuck = "thefuck --repeat --force-command 'ls -l'"
    expected = f"ls -l || {repeat_fuck}"

    assert corr._get_script() == expected

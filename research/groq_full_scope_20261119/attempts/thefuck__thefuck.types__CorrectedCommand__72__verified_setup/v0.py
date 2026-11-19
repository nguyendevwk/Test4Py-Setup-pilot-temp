import sys
import os
import builtins
import types
import contextlib

import pytest

from thefuck.types import CorrectedCommand
from thefuck import settings
from thefuck import shell


@pytest.fixture(autouse=True)
def restore_settings():
    """Restore settings after each test."""
    original_repeat = settings.repeat
    original_debug = settings.debug
    original_alter_history = settings.alter_history
    yield
    settings.repeat = original_repeat
    settings.debug = original_debug
    settings.alter_history = original_alter_history


def test_eq_and_hash_and_repr():
    """CorrectedCommand equality ignores priority and hash is consistent."""
    cmd1 = CorrectedCommand("ls", None, 10)
    cmd2 = CorrectedCommand("ls", None, 5)
    cmd3 = CorrectedCommand("cat", None, 10)

    # Equality ignores priority
    assert cmd1 == cmd2
    assert cmd1 != cmd3

    # Hash is based on script and side_effect
    assert hash(cmd1) == hash(cmd2)
    assert hash(cmd1) != hash(cmd3)

    # Representation includes all fields
    rep = repr(cmd1)
    assert "CorrectedCommand" in rep
    assert "ls" in rep
    assert "10" in rep


def test_get_script_repeat_behavior(tmp_path):
    """_get_script returns correct script depending on settings.repeat."""
    # Ensure repeat is False
    settings.repeat = False
    cmd = CorrectedCommand("echo hello", None, 1)
    assert cmd._get_script() == "echo hello"

    # Enable repeat and debug
    settings.repeat = True
    settings.debug = True
    # Use a simple script that contains no spaces
    cmd = CorrectedCommand("echo world", None, 1)
    result = cmd._get_script()
    # The result should contain the original script and the repeat command
    assert "echo world" in result
    # The repeat command should include the alias and force-command
    assert "--force-command" in result
    # The debug flag should be present
    assert "--debug" in result


def test_run_writes_stdout_and_side_effect(monkeypatch, capsys):
    """run writes the script to stdout and calls side_effect."""
    # Prepare a side_effect that records its arguments
    called = {}
    def side_effect(old_cmd, script):
        called['old_cmd'] = old_cmd
        called['script'] = script

    # Disable history alteration to avoid side effects on the real history
    settings.alter_history = False
    settings.repeat = False

    cmd = CorrectedCommand("printf 'test'", side_effect, 1)

    # Create a dummy old_cmd object
    class DummyCommand:
        pass
    old_cmd = DummyCommand()

    # Run the command
    cmd.run(old_cmd)

    # Capture stdout
    captured = capsys.readouterr()
    assert captured.out.strip() == "printf 'test'"

    # Verify side_effect was called with correct arguments
    assert called['old_cmd'] is old_cmd
    assert called['script'] == "printf 'test'"

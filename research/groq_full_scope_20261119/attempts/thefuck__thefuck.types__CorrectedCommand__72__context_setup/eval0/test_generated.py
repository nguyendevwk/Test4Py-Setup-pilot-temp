import sys
import os
import builtins
import types
import pytest

from thefuck.types import CorrectedCommand
from thefuck import settings
from thefuck import shell


def _reset_settings():
    """Restore settings to defaults after a test."""
    settings.repeat = False
    settings.debug = False
    settings.alter_history = False


def test_eq_and_hash_and_repr():
    """CorrectedCommand equality ignores priority and hash is consistent."""
    cmd1 = CorrectedCommand("ls", None, 10)
    cmd2 = CorrectedCommand("ls", None, 20)
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
    """_get_script returns original script or repeats based on settings."""
    # Ensure repeat is False
    settings.repeat = False
    cmd = CorrectedCommand("echo hi", None, 0)
    assert cmd._get_script() == "echo hi"

    # Enable repeat and debug
    settings.repeat = True
    settings.debug = True
    # Use a simple script that contains spaces
    script = "echo 'hello world'"
    cmd = CorrectedCommand(script, None, 0)
    result = cmd._get_script()
    # Should contain the original script and the repeat wrapper
    assert script in result
    # The repeat wrapper should include the alias and --debug flag
    alias = shell.get_alias()
    assert alias in result
    assert "--debug" in result
    # The repeat wrapper should be quoted correctly
    quoted = shell.quote(script)
    assert quoted in result
    # Clean up
    _reset_settings()


def test_run_writes_to_stdout_and_side_effect(monkeypatch, capsys):
    """run writes the script to stdout and calls side_effect."""
    # Prepare a side_effect that records its arguments
    recorded = {}
    def side_effect(old_cmd, new_script):
        recorded['old'] = old_cmd
        recorded['new'] = new_script

    # Use a dummy old_cmd object
    class DummyCmd:
        pass
    old_cmd = DummyCmd()

    # Ensure history alteration is disabled to avoid file writes
    settings.alter_history = False
    cmd = CorrectedCommand("pwd", side_effect, 0)

    # Run the command
    cmd.run(old_cmd)

    # Capture stdout
    out, err = capsys.readouterr()
    assert out.strip() == "pwd"

    # Side effect should have been called with correct arguments
    assert recorded['old'] is old_cmd
    assert recorded['new'] == "pwd"

    # Clean up
    _reset_settings()

import os
import sys
import pytest
from thefuck.types import CorrectedCommand
from thefuck.conf import settings
from thefuck.shells import shell
from thefuck.utils import get_alias

# Helper side effect that records calls
class SideEffectRecorder:
    def __init__(self):
        self.calls = []

    def __call__(self, old_cmd, script):
        self.calls.append((old_cmd, script))

def test_corrected_command_equality_and_hash():
    """CorrectedCommand equality ignores priority and hash is consistent."""
    side_effect = SideEffectRecorder()
    cmd1 = CorrectedCommand("echo hi", side_effect, priority=10)
    cmd2 = CorrectedCommand("echo hi", side_effect, priority=20)
    cmd3 = CorrectedCommand("echo bye", side_effect, priority=10)

    # Equality ignores priority
    assert cmd1 == cmd2
    assert cmd1 != cmd3

    # Hash is based on script and side_effect
    assert hash(cmd1) == hash(cmd2)
    assert hash(cmd1) != hash(cmd3)

def test_corrected_command_repr_and_run(monkeypatch, tmp_path):
    """__repr__ shows all fields and run writes the script."""
    # Prepare a dummy old command
    class DummyCommand:
        def __init__(self, text):
            self.text = text
    old_cmd = DummyCommand("wrong command")

    # Capture stdout
    output = []

    def fake_write(s):
        output.append(s)

    monkeypatch.setattr(sys.stdout, "write", fake_write)

    # Ensure history is not altered
    monkeypatch.setattr(settings, "alter_history", False)

    # Use a simple side effect that does nothing
    side_effect = None
    cmd = CorrectedCommand("corrected command", side_effect, priority=5)

    # Check repr
    expected_repr = "CorrectedCommand(script=corrected command, side_effect=None, priority=5)"
    assert repr(cmd) == expected_repr

    # Run the command
    cmd.run(old_cmd)
    # The script should be written to stdout
    assert output == ["corrected command"]

def test_corrected_command_get_script_repeat(monkeypatch):
    """_get_script appends repeat command when settings.repeat is True."""
    # Set repeat and debug flags
    monkeypatch.setattr(settings, "repeat", True)
    monkeypatch.setattr(settings, "debug", False)

    # Mock get_alias to return a known alias
    monkeypatch.setattr("thefuck.utils.get_alias", lambda: "fuck")

    # Mock shell.quote to return quoted script
    monkeypatch.setattr(shell, "quote", lambda s: f"'{s}'")

    # Mock shell.or_ to join commands with " || "
    monkeypatch.setattr(shell, "or_", lambda a, b: f"{a} || {b}")

    cmd = CorrectedCommand("ls -l", None, priority=1)
    script = cmd._get_script()
    expected_repeat = "fuck --repeat  --force-command 'ls -l'"
    expected_script = f"ls -l || {expected_repeat}"
    assert script == expected_script

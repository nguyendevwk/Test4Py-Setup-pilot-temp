import sys
import types as pytypes
import argparse
import pytest

# Import the target module
from thefuck.entrypoints import fix_command as target_module

# Helper to create a dummy command object
class DummyCommand:
    def __init__(self):
        self.ran = False
    def run(self, _):
        self.ran = True

def test_fix_command_empty_command(monkeypatch, capsys):
    """When the raw command is empty, the function should return without exiting."""
    # Prepare known_args with a dummy history file path
    known_args = argparse.Namespace(history_file="dummy_history")
    # Patch settings.init to a no-op
    monkeypatch.setattr(target_module.settings, "init", lambda _: None)
    # Patch _get_raw_command to return an empty string
    monkeypatch.setattr(target_module, "_get_raw_command", lambda _: "")
    # Patch types.Command.from_raw_script to raise EmptyCommand
    monkeypatch.setattr(target_module.types.Command, "from_raw_script",
                       lambda _: (_ for _ in ()).throw(target_module.EmptyCommand()))
    # Run the function
    result = target_module.fix_command(known_args)
    # It should return None and not exit
    assert result is None
    # Capture output to ensure debug message is printed
    captured = capsys.readouterr()
    assert "Empty command" in captured.out

def test_fix_command_no_selection(monkeypatch):
    """When no command is selected, the function should exit with status 1."""
    known_args = argparse.Namespace(history_file="dummy_history")
    monkeypatch.setattr(target_module.settings, "init", lambda _: None)
    monkeypatch.setattr(target_module, "_get_raw_command", lambda _: "echo hello")
    # Provide a valid command object
    dummy_cmd = pytypes.SimpleNamespace()
    monkeypatch.setattr(target_module.types.Command, "from_raw_script",
                       lambda _: dummy_cmd)
    # get_corrected_commands returns a list but select_command returns None
    monkeypatch.setattr(target_module, "get_corrected_commands", lambda _: [DummyCommand()])
    monkeypatch.setattr(target_module, "select_command", lambda _: None)
    with pytest.raises(SystemExit) as excinfo:
        target_module.fix_command(known_args)
    assert excinfo.value.code == 1

def test_fix_command_success(monkeypatch):
    """When a corrected command is selected, it should be run."""
    known_args = argparse.Namespace(history_file="dummy_history")
    monkeypatch.setattr(target_module.settings, "init", lambda _: None)
    monkeypatch.setattr(target_module, "_get_raw_command", lambda _: "echo hello")
    dummy_cmd = pytypes.SimpleNamespace()
    monkeypatch.setattr(target_module.types.Command, "from_raw_script",
                       lambda _: dummy_cmd)
    dummy_corrected = DummyCommand()
    monkeypatch.setattr(target_module, "get_corrected_commands", lambda _: [dummy_corrected])
    monkeypatch.setattr(target_module, "select_command", lambda _: dummy_corrected)
    target_module.fix_command(known_args)
    assert dummy_corrected.ran is True

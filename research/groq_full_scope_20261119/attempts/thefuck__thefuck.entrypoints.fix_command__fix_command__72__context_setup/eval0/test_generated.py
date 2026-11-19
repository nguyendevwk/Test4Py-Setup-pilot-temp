import builtins
import sys
import types as pytypes
import pytest
from thefuck.entrypoints.fix_command import fix_command, _get_raw_command
from thefuck import logs, settings, const, types, conf, corrector, ui, utils

# Helper objects for tests
class DummyCommand:
    def __init__(self, script):
        self.script = script
    def run(self, original):
        self.executed_with = original

class DummyKnownArgs(pytypes.SimpleNamespace):
    def __init__(self, force_command=None, command=None):
        super().__init__(force_command=force_command, command=command)

@pytest.fixture
def monkeypatch_settings(monkeypatch):
    monkeypatch.setattr(settings, "init", lambda *_, **__: None)

def test_fix_command_empty_command(monkeypatch, monkeypatch_settings):
    """When Command.from_raw_script raises EmptyCommand, fix_command returns None."""
    known_args = DummyKnownArgs(command=["echo", "hi"])
    monkeypatch.setattr(types.Command, "from_raw_script", lambda _: (_ for _ in ()).throw(conf.EmptyCommand()))
    # Ensure no side effects
    monkeypatch.setattr(corrector, "get_corrected_commands", lambda _: [])
    monkeypatch.setattr(ui, "select_command", lambda _: None)
    result = fix_command(known_args)
    assert result is None

def test_fix_command_runs_selected(monkeypatch, monkeypatch_settings, tmp_path):
    """When a corrected command is selected, its run method is called with the original command."""
    known_args = DummyKnownArgs(force_command=["echo", "test"])
    # Mock Command.from_raw_script to return a DummyCommand
    original_cmd = DummyCommand("echo test")
    monkeypatch.setattr(types.Command, "from_raw_script", lambda _: original_cmd)
    # Provide a corrected command that will be selected
    corrected = DummyCommand("echo corrected")
    monkeypatch.setattr(corrector, "get_corrected_commands", lambda _: [corrected])
    monkeypatch.setattr(ui, "select_command", lambda _: corrected)
    # Capture logs to avoid clutter
    monkeypatch.setattr(logs, "debug_time", lambda *_, **__: pytypes.SimpleNamespace(__enter__=lambda self: None, __exit__=lambda *__: None))
    fix_command(known_args)
    assert hasattr(corrected, "executed_with")
    assert corrected.executed_with is original_cmd

def test_fix_command_no_selection_exits(monkeypatch, monkeypatch_settings):
    """When no command is selected, fix_command exits with status 1."""
    known_args = DummyKnownArgs(command=["false"])
    monkeypatch.setattr(types.Command, "from_raw_script", lambda _: DummyCommand("false"))
    monkeypatch.setattr(corrector, "get_corrected_commands", lambda _: [])
    monkeypatch.setattr(ui, "select_command", lambda _: None)
    monkeypatch.setattr(logs, "debug_time", lambda *_, **__: pytypes.SimpleNamespace(__enter__=lambda self: None, __exit__=lambda *__: None))
    with pytest.raises(SystemExit) as excinfo:
        fix_command(known_args)
    assert excinfo.value.code == 1

import builtins
import sys
import types as pytypes
import pytest
from thefuck.entrypoints.fix_command import fix_command
from thefuck import logs, const, settings, types, exceptions, ui, utils, corrector

# Helper to create a dummy command object
class DummyCommand:
    def __init__(self):
        self.ran = False
    def run(self, _):
        self.ran = True

def test_fix_command_empty_command(monkeypatch):
    """When Command.from_raw_script raises EmptyCommand, fix_command returns None."""
    dummy_settings = pytypes.SimpleNamespace()
    monkeypatch.setattr(settings, "init", lambda _: None)
    monkeypatch.setattr(const, "RAW_COMMAND", "dummy")
    monkeypatch.setattr(utils, "get_alias", lambda _: None)
    monkeypatch.setattr(utils, "get_all_executables", lambda: [])
    monkeypatch.setattr(types.Command, "from_raw_script", lambda _: (_ for _ in ()).throw(exceptions.EmptyCommand()))
    monkeypatch.setattr(ui, "select_command", lambda _: None)
    monkeypatch.setattr(corrector, "get_corrected_commands", lambda _: [])
    # Ensure _get_raw_command returns something
    monkeypatch.setattr(fix_command, "_get_raw_command", lambda _: "dummy")
    result = fix_command([])
    assert result is None

def test_fix_command_no_corrections(monkeypatch):
    """When no corrected commands are available, fix_command exits with status 1."""
    dummy_settings = pytypes.SimpleNamespace()
    monkeypatch.setattr(settings, "init", lambda _: None)
    monkeypatch.setattr(const, "RAW_COMMAND", "dummy")
    monkeypatch.setattr(utils, "get_alias", lambda _: None)
    monkeypatch.setattr(utils, "get_all_executables", lambda: [])
    monkeypatch.setattr(types.Command, "from_raw_script", lambda _: DummyCommand())
    monkeypatch.setattr(ui, "select_command", lambda _: None)
    monkeypatch.setattr(corrector, "get_corrected_commands", lambda _: [])
    monkeypatch.setattr(fix_command, "_get_raw_command", lambda _: "dummy")
    with pytest.raises(SystemExit) as excinfo:
        fix_command([])
    assert excinfo.value.code == 1

def test_fix_command_success(monkeypatch):
    """When a correction is selected, its run method is called."""
    dummy_settings = pytypes.SimpleNamespace()
    monkeypatch.setattr(settings, "init", lambda _: None)
    monkeypatch.setattr(const, "RAW_COMMAND", "dummy")
    monkeypatch.setattr(utils, "get_alias", lambda _: None)
    monkeypatch.setattr(utils, "get_all_executables", lambda: [])
    dummy_cmd = DummyCommand()
    monkeypatch.setattr(types.Command, "from_raw_script", lambda _: dummy_cmd)
    selected = DummyCommand()
    monkeypatch.setattr(ui, "select_command", lambda _: selected)
    monkeypatch.setattr(corrector, "get_corrected_commands", lambda _: [selected])
    monkeypatch.setattr(fix_command, "_get_raw_command", lambda _: "dummy")
    fix_command([])
    assert selected.ran is True

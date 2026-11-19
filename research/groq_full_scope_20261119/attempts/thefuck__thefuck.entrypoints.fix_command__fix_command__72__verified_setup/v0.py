import sys
import types as pytypes
import pytest
from thefuck.entrypoints.fix_command import fix_command, _get_raw_command
from thefuck import logs, settings, types, const, conf, corrector, ui, utils, exceptions

# Dummy command object used in tests
class DummyCommand:
    def __init__(self):
        self.ran = False
    def run(self, _):
        self.ran = True

@pytest.fixture
def patch_module(monkeypatch):
    # Disable real settings initialization
    monkeypatch.setattr(settings, "init", lambda _: None)
    # Replace debug_time context manager with a no-op
    class DummyContext:
        def __enter__(self): return None
        def __exit__(self, exc_type, exc, tb): return False
    monkeypatch.setattr(logs, "debug_time", lambda *_, **__: DummyContext())
    # Ensure _get_raw_command can be patched
    monkeypatch.setattr(fix_command, "_get_raw_command", lambda _: None)

def test_fix_command_empty_command_returns_none(patch_module, monkeypatch):
    # Simulate empty command by raising EmptyCommand
    monkeypatch.setattr(_get_raw_command, "__call__", lambda _: "")
    monkeypatch.setattr(types.Command, "from_raw_script", lambda _: (_ for _ in ()).throw(exceptions.EmptyCommand()))
    # Capture return value
    result = fix_command([])
    assert result is None

def test_fix_command_no_corrections_exits(patch_module, monkeypatch):
    # Simulate a command that yields no corrections
    monkeypatch.setattr(_get_raw_command, "__call__", lambda _: "badcmd")
    dummy_cmd = DummyCommand()
    monkeypatch.setattr(types.Command, "from_raw_script", lambda _: dummy_cmd)
    monkeypatch.setattr(corrector, "get_corrected_commands", lambda _: [])
    # select_command should not be called; patch to raise if called
    monkeypatch.setattr(ui, "select_command", lambda _: (_ for _ in ()).throw(RuntimeError("select_command called")))
    with pytest.raises(SystemExit) as excinfo:
        fix_command([])
    assert excinfo.value.code == 1

def test_fix_command_runs_selected_command(patch_module, monkeypatch):
    # Simulate a command with one correction
    monkeypatch.setattr(_get_raw_command, "__call__", lambda _: "badcmd")
    dummy_cmd = DummyCommand()
    monkeypatch.setattr(types.Command, "from_raw_script", lambda _: dummy_cmd)
    corrected = [DummyCommand()]
    monkeypatch.setattr(corrector, "get_corrected_commands", lambda _: corrected)
    # select_command returns the first corrected command
    monkeypatch.setattr(ui, "select_command", lambda _: corrected[0])
    # Run the function
    fix_command([])
    # Verify that the selected command's run method was invoked
    assert corrected[0].ran is True

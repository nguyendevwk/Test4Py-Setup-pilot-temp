import builtins
import sys
import types as pytypes
import pytest

from thefuck.entrypoints.fix_command import fix_command
from thefuck import logs, const, settings, types, exceptions, ui, utils, corrector, conf

# Helper to create a dummy command object with a run method
class DummyCommand:
    def __init__(self):
        self.ran = False
    def run(self, _):
        self.ran = True

@pytest.fixture
def monkeypatch_settings(monkeypatch):
    # Make settings.init a no-op
    monkeypatch.setattr(settings, "init", lambda _: None)

@pytest.fixture
def monkeypatch_get_raw_command(monkeypatch):
    # Return a dummy raw command string
    monkeypatch.setattr("thefuck.entrypoints.fix_command._get_raw_command", lambda _: "dummy command")

def test_fix_command_empty_command(monkeypatch, monkeypatch_settings, monkeypatch_get_raw_command):
    # Simulate EmptyCommand being raised
    monkeypatch.setattr(types.Command, "from_raw_script", lambda _: (_ for _ in ()).throw(exceptions.EmptyCommand()))
    # Capture logs output
    with logs.debug_time("Total"):
        result = fix_command(known_args=pytypes.SimpleNamespace())
    assert result is None

def test_fix_command_no_corrections(monkeypatch, monkeypatch_settings, monkeypatch_get_raw_command):
    # Normal command parsing
    monkeypatch.setattr(types.Command, "from_raw_script", lambda _: pytypes.SimpleNamespace())
    # No corrected commands
    monkeypatch.setattr(corrector, "get_corrected_commands", lambda _: [])
    # select_command returns None
    monkeypatch.setattr(ui, "select_command", lambda _: None)
    with pytest.raises(SystemExit) as excinfo:
        fix_command(known_args=pytypes.SimpleNamespace())
    assert excinfo.value.code == 1

def test_fix_command_success(monkeypatch, monkeypatch_settings, monkeypatch_get_raw_command):
    # Normal command parsing
    monkeypatch.setattr(types.Command, "from_raw_script", lambda _: pytypes.SimpleNamespace())
    dummy = DummyCommand()
    # Provide one corrected command
    monkeypatch.setattr(corrector, "get_corrected_commands", lambda _: [dummy])
    # select_command returns the dummy command
    monkeypatch.setattr(ui, "select_command", lambda _: dummy)
    # Run the function
    fix_command(known_args=pytypes.SimpleNamespace())
    assert dummy.ran is True

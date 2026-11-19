import builtins
import sys
import types as pytypes
import pytest
from thefuck.entrypoints.fix_command import fix_command, _get_raw_command
from thefuck import logs, settings, const, conf

# Helper to create a simple argparse-like object
class Args:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

# Dummy command object with a run method
class DummyCommand:
    def __init__(self):
        self.ran = False
    def run(self, _):
        self.ran = True

# Test normal flow: a command is corrected and run
def test_fix_command_runs_corrected(monkeypatch):
    # Prepare known_args
    known_args = Args(force_command=None, command=['echo', 'hello'])
    # Patch settings.init to do nothing
    monkeypatch.setattr(settings, 'init', lambda _: None)
    # Patch types.Command.from_raw_script to return a dummy command
    dummy_cmd = DummyCommand()
    monkeypatch.setattr('thefuck.types.Command.from_raw_script', lambda raw: dummy_cmd)
    # Patch get_corrected_commands to return a list with a dummy command
    corrected = [DummyCommand()]
    monkeypatch.setattr('thefuck.corrector.get_corrected_commands', lambda cmd: corrected)
    # Patch select_command to return the first corrected command
    monkeypatch.setattr('thefuck.ui.select_command', lambda cmds: cmds[0])
    # Capture logs
    with logs.debug_time('Total'):
        fix_command(known_args)
    # Assert that the selected command's run was called
    assert corrected[0].ran

# Test that EmptyCommand causes no action and no exit
def test_fix_command_empty_command(monkeypatch):
    known_args = Args(force_command=None, command=[''])
    monkeypatch.setattr(settings, 'init', lambda _: None)
    # Simulate EmptyCommand being raised
    monkeypatch.setattr('thefuck.types.Command.from_raw_script', lambda raw: (_ for _ in ()).throw(conf.EmptyCommand()))
    # Ensure get_corrected_commands is not called
    called = False
    def fake_get(cmd):
        nonlocal called
        called = True
        return []
    monkeypatch.setattr('thefuck.corrector.get_corrected_commands', fake_get)
    # Run and ensure no exception
    fix_command(known_args)
    assert not called

# Test that when no command is selected, the program exits with code 1
def test_fix_command_no_selection(monkeypatch):
    known_args = Args(force_command=None, command=['badcmd'])
    monkeypatch.setattr(settings, 'init', lambda _: None)
    monkeypatch.setattr('thefuck.types.Command.from_raw_script', lambda raw: DummyCommand())
    monkeypatch.setattr('thefuck.corrector.get_corrected_commands', lambda cmd: [DummyCommand()])
    # select_command returns None to simulate user abort
    monkeypatch.setattr('thefuck.ui.select_command', lambda cmds: None)
    with pytest.raises(SystemExit) as excinfo:
        fix_command(known_args)
    assert excinfo.value.code == 1

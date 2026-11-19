import pytest
from thefuck.rules.vagrant_up import get_new_command
from thefuck.shells import shell

class DummyCommand:
    def __init__(self, script):
        self.script = script
        self.script_parts = script.split()

def test_get_new_command_no_machine():
    cmd = DummyCommand("vagrant up")
    new_cmds = get_new_command(cmd)
    assert isinstance(new_cmds, shell.ShellCommand)
    assert new_cmds.script == "vagrant up"

def test_get_new_command_with_machine():
    cmd = DummyCommand("vagrant up myvm")
    new_cmds = get_new_command(cmd)
    assert isinstance(new_cmds, list)
    assert len(new_cmds) == 2
    assert new_cmds[0].script == "vagrant up myvm"
    assert new_cmds[1].script == "vagrant up"

def test_get_new_command_boundary_len_three():
    cmd = DummyCommand("vagrant up myvm extra")
    new_cmds = get_new_command(cmd)
    assert isinstance(new_cmds, list)
    assert len(new_cmds) == 2
    assert new_cmds[0].script == "vagrant up myvm"
    assert new_cmds[1].script == "vagrant up"

import pytest
from thefuck.rules.vagrant_up import get_new_command
from thefuck.shells import shell

class DummyCommand:
    def __init__(self, script, parts):
        self.script = script
        self.script_parts = parts

def test_get_new_command_no_machine():
    """When the command has fewer than 3 parts, it should return a single
    'vagrant up' command."""
    cmd = DummyCommand("vagrant status", ["vagrant", "status"])
    new_cmd = get_new_command(cmd)
    assert isinstance(new_cmd, shell.ShellCommand)
    assert new_cmd.script == "vagrant up"

def test_get_new_command_with_machine():
    """When the command has at least 3 parts, it should return a list of two
    commands: one targeting the specific machine and one generic."""
    cmd = DummyCommand("vagrant status web", ["vagrant", "status", "web"])
    new_cmds = get_new_command(cmd)
    assert isinstance(new_cmds, list)
    assert len(new_cmds) == 2
    # First command targets the machine
    assert new_cmds[0].script == "vagrant up web"
    # Second command is generic
    assert new_cmds[1].script == "vagrant up"

def test_get_new_command_boundary_length():
    """Boundary test where the command has exactly 3 parts."""
    cmd = DummyCommand("vagrant up", ["vagrant", "up"])
    new_cmd = get_new_command(cmd)
    assert isinstance(new_cmd, shell.ShellCommand)
    assert new_cmd.script == "vagrant up"

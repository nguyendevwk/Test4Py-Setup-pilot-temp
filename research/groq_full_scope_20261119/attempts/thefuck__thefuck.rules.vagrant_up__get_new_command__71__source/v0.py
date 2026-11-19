import pytest
from thefuck.rules.vagrant_up import get_new_command
from thefuck.shells import shell

class DummyCommand:
    def __init__(self, script, parts):
        self.script = script
        self.script_parts = parts

def test_get_new_command_no_machine():
    # Command with fewer than 3 parts: no machine specified
    cmd = DummyCommand("vagrant up", ["vagrant", "up"])
    result = get_new_command(cmd)
    # Should return a single command that starts all instances
    assert isinstance(result, shell.Command)
    assert result.command == "vagrant up"
    assert result.script == "vagrant up"

def test_get_new_command_with_machine():
    # Command with a machine name at index 2
    cmd = DummyCommand("vagrant up web", ["vagrant", "up", "web"])
    result = get_new_command(cmd)
    # Should return a list of two commands
    assert isinstance(result, list)
    assert len(result) == 2
    # First command should target the specific machine
    assert result[0].command == "vagrant up web"
    assert result[0].script == "vagrant up web"
    # Second command should start all instances
    assert result[1].command == "vagrant up"
    assert result[1].script == "vagrant up"

def test_get_new_command_with_extra_parts():
    # Command with more than 3 parts: machine still taken from index 2
    cmd = DummyCommand("vagrant up db --provision", ["vagrant", "up", "db", "--provision"])
    result = get_new_command(cmd)
    # Should behave like the previous case
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0].command == "vagrant up db"
    assert result[0].script == "vagrant up db"
    assert result[1].command == "vagrant up"
    assert result[1].script == "vagrant up"

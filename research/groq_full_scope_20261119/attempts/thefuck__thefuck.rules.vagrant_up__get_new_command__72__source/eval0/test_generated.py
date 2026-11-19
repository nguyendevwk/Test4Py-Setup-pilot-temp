import pytest
from thefuck.rules.vagrant_up import get_new_command
from thefuck.shells import shell

class DummyCommand:
    def __init__(self, script: str):
        self.script = script
        self.script_parts = script.split()

def test_get_new_command_no_machine(tmp_path):
    # Command with fewer than 3 parts -> no machine specified
    cmd = DummyCommand("vagrant status")
    result = get_new_command(cmd)
    # Should return a single shell.and_ command that starts all instances
    assert isinstance(result, shell.ShellCommand)
    assert result.script == "vagrant up vagrant status"

def test_get_new_command_with_machine(tmp_path):
    # Command with a machine name as the third part
    cmd = DummyCommand("vagrant up webserver")
    result = get_new_command(cmd)
    # Should return a list of two shell.and_ commands
    assert isinstance(result, list)
    assert len(result) == 2
    # First command targets the specific machine
    assert isinstance(result[0], shell.ShellCommand)
    assert result[0].script == "vagrant up webserver vagrant up webserver"
    # Second command starts all instances
    assert isinstance(result[1], shell.ShellCommand)
    assert result[1].script == "vagrant up vagrant up webserver"

def test_get_new_command_boundary_cases(tmp_path):
    # Command with exactly 3 parts but machine is empty string
    cmd = DummyCommand("vagrant up ")
    result = get_new_command(cmd)
    # machine will be '' (empty string), treated as specified
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0].script == "vagrant up  vagrant up "
    assert result[1].script == "vagrant up vagrant up "

import pytest
from thefuck.rules.vagrant_up import get_new_command
from thefuck.shells import shell


class DummyCommand:
    def __init__(self, script):
        self.script = script
        self.script_parts = script.split()


def test_get_new_command_no_machine(tmp_path):
    # Command with only two parts: "vagrant up"
    cmd = DummyCommand("vagrant up")
    result = get_new_command(cmd)
    # Should return a single ShellCommand that starts all instances
    assert isinstance(result, shell.ShellCommand)
    assert result.script == "vagrant up"


def test_get_new_command_with_machine(tmp_path):
    # Command with a machine name: "vagrant up mymachine"
    cmd = DummyCommand("vagrant up mymachine")
    result = get_new_command(cmd)
    # Should return a list of two ShellCommands
    assert isinstance(result, list)
    assert len(result) == 2
    # First command starts the specific machine
    assert isinstance(result[0], shell.ShellCommand)
    assert result[0].script == "vagrant up mymachine"
    # Second command starts all instances
    assert isinstance(result[1], shell.ShellCommand)
    assert result[1].script == "vagrant up"


def test_get_new_command_edge_case_empty_script(tmp_path):
    # Empty script should still return a ShellCommand that starts all instances
    cmd = DummyCommand("")
    result = get_new_command(cmd)
    assert isinstance(result, shell.ShellCommand)
    assert result.script == "vagrant up"

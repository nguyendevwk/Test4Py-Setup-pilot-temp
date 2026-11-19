import pytest
from thefuck.rules.vagrant_up import get_new_command
from thefuck.shells import shell

class DummyCommand:
    def __init__(self, script):
        self.script = script
        self.script_parts = script.split()

def test_get_new_command_no_machine():
    cmd = DummyCommand("vagrant status")
    new_cmd = get_new_command(cmd)
    # When no machine part, should return a single command string
    assert isinstance(new_cmd, str)
    assert new_cmd == shell.and_(u"vagrant up", cmd.script)

def test_get_new_command_with_machine():
    cmd = DummyCommand("vagrant up myvm")
    new_cmd = get_new_command(cmd)
    # Should return a list of two command strings
    assert isinstance(new_cmd, list)
    assert len(new_cmd) == 2
    # First command includes the machine name
    assert new_cmd[0] == shell.and_(u"vagrant up myvm", cmd.script)
    # Second command is the generic start_all_instances
    assert new_cmd[1] == shell.and_(u"vagrant up", cmd.script)

def test_get_new_command_with_extra_parts():
    cmd = DummyCommand("vagrant up myvm --provision")
    new_cmd = get_new_command(cmd)
    # Even with extra parts, machine is taken from index 2
    assert isinstance(new_cmd, list)
    assert len(new_cmd) == 2
    assert new_cmd[0] == shell.and_(u"vagrant up myvm", cmd.script)
    assert new_cmd[1] == shell.and_(u"vagrant up", cmd.script)

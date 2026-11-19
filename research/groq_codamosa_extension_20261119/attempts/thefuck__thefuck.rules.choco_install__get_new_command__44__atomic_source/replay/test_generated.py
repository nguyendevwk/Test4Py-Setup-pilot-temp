import pytest
from thefuck.rules.choco_install import get_new_command

class DummyCommand:
    def __init__(self, script):
        self.script = script
        self.script_parts = script.split()

def test_get_new_command_replaces_package_name():
    cmd = DummyCommand("choco install git")
    new_cmd = get_new_command(cmd)
    assert new_cmd == "choco install git.install"

def test_get_new_command_handles_hyphenated_package():
    cmd = DummyCommand("choco install git-foo")
    new_cmd = get_new_command(cmd)
    assert new_cmd == "choco install git-foo.install"

def test_get_new_command_returns_empty_when_no_package():
    cmd = DummyCommand("choco install -y")
    new_cmd = get_new_command(cmd)
    assert new_cmd == []

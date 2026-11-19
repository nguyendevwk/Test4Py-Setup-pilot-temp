import pytest
from thefuck.rules.choco_install import get_new_command

class DummyCommand:
    def __init__(self, script):
        self.script = script
        self.script_parts = script.split()

def test_get_new_command_replaces_package_name():
    # Normal case: package name is 'git'
    cmd = DummyCommand("choco install git")
    new_cmd = get_new_command(cmd)
    assert new_cmd == "choco install git.install"

def test_get_new_command_no_package_name_returns_empty_list():
    # Boundary case: only options, no package name
    cmd = DummyCommand("choco install -y")
    new_cmd = get_new_command(cmd)
    assert new_cmd == []

def test_get_new_command_handles_multiple_parts_and_parameters():
    # Normal case with multiple parts: 'cinst' command with a package and a flag
    cmd = DummyCommand("cinst python -y")
    new_cmd = get_new_command(cmd)
    assert new_cmd == "cinst python.install -y"

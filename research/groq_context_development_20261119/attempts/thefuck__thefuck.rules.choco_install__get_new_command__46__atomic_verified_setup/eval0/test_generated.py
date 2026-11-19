import pytest
from thefuck.rules.choco_install import get_new_command
from thefuck.utils import for_app, which

class DummyCommand:
    def __init__(self, script):
        self.script = script
        self.script_parts = script.split()

def test_get_new_command_replaces_package_name():
    cmd = DummyCommand("choco install git")
    new_cmd = get_new_command(cmd)
    assert new_cmd == "choco install git.install"

def test_get_new_command_returns_empty_for_only_parameters():
    cmd = DummyCommand("choco install -y --no-progress")
    new_cmd = get_new_command(cmd)
    assert new_cmd == []

def test_get_new_command_skips_invalid_package_parts():
    cmd = DummyCommand("choco install chocolatey=1.0")
    new_cmd = get_new_command(cmd)
    assert new_cmd == []

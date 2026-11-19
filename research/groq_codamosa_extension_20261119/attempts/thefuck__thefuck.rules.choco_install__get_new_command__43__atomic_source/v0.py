import pytest
from thefuck.rules.choco_install import get_new_command

class DummyCommand:
    def __init__(self, script, script_parts):
        self.script = script
        self.script_parts = script_parts

def test_get_new_command_replaces_first_valid_part():
    cmd = DummyCommand(
        script="choco install git",
        script_parts=["choco", "install", "git"]
    )
    new_cmd = get_new_command(cmd)
    assert new_cmd == "choco install git.install"

def test_get_new_command_returns_empty_when_no_valid_part():
    cmd = DummyCommand(
        script="choco install -y git",
        script_parts=["choco", "install", "-y", "git"]
    )
    new_cmd = get_new_command(cmd)
    assert new_cmd == []

def test_get_new_command_handles_empty_script_parts():
    cmd = DummyCommand(
        script="choco install",
        script_parts=[]
    )
    new_cmd = get_new_command(cmd)
    assert new_cmd == []

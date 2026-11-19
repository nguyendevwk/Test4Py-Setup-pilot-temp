import pytest
from thefuck.rules.choco_install import get_new_command

class DummyCommand:
    def __init__(self, script, script_parts):
        self.script = script
        self.script_parts = script_parts

def test_get_new_command_replaces_package_name():
    # Normal case: command contains a package name that should be replaced
    cmd = DummyCommand(
        script="choco install git",
        script_parts=["choco", "install", "git"]
    )
    new_cmd = get_new_command(cmd)
    assert new_cmd == "choco install git.install"

def test_get_new_command_no_package_name_returns_empty_list():
    # Boundary case: command contains only options, no package name
    cmd = DummyCommand(
        script="choco install -y",
        script_parts=["choco", "install", "-y"]
    )
    new_cmd = get_new_command(cmd)
    assert new_cmd == []

def test_get_new_command_package_name_with_special_chars():
    # Error-like case: package name contains a hyphen but should still be replaced
    cmd = DummyCommand(
        script="cinst my-package",
        script_parts=["cinst", "my-package"]
    )
    new_cmd = get_new_command(cmd)
    assert new_cmd == "cinst my-package.install"

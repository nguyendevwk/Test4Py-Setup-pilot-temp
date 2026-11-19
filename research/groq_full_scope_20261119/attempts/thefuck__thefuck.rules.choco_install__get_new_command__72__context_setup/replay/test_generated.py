import pytest
from thefuck.rules.choco_install import get_new_command

class DummyCommand:
    def __init__(self, script, script_parts):
        self.script = script
        self.script_parts = script_parts

def test_get_new_command_replaces_package_name():
    # Command with a clear package name "git"
    cmd = DummyCommand(
        script="choco install git",
        script_parts=["choco", "install", "git"]
    )
    new_cmd = get_new_command(cmd)
    assert new_cmd == "choco install git.install"
    # Ensure only the package part was modified
    assert "git.install" in new_cmd
    assert "git" not in new_cmd.replace("git.install", "")

def test_get_new_command_no_package_returns_empty_list():
    # Command that contains only options and no package name
    cmd = DummyCommand(
        script="choco install -y",
        script_parts=["choco", "install", "-y"]
    )
    new_cmd = get_new_command(cmd)
    assert new_cmd == []

def test_get_new_command_package_with_special_chars():
    # Package name that includes a hyphen but is not a parameter
    cmd = DummyCommand(
        script="cinst nodejs.install",
        script_parts=["cinst", "nodejs.install"]
    )
    new_cmd = get_new_command(cmd)
    # The function should treat "nodejs.install" as the package name
    assert new_cmd == "cinst nodejs.install.install"
    # Verify that the original script was correctly replaced
    assert new_cmd.endswith("nodejs.install.install")

import pytest
from thefuck.rules.choco_install import get_new_command


class DummyCommand:
    def __init__(self, script, script_parts):
        self.script = script
        self.script_parts = script_parts


def test_get_new_command_appends_install_to_package_name():
    # Normal case: the package name is "myapp"
    cmd = DummyCommand(
        script="choco install myapp",
        script_parts=["choco", "install", "myapp"]
    )
    new_cmd = get_new_command(cmd)
    assert new_cmd == "choco install myapp.install"
    # Ensure the original command is unchanged
    assert cmd.script == "choco install myapp"


def test_get_new_command_returns_empty_list_when_no_package_name():
    # Boundary case: all parts are excluded (only options and commands)
    cmd = DummyCommand(
        script="choco install -y --no-progress",
        script_parts=["choco", "install", "-y", "--no-progress"]
    )
    new_cmd = get_new_command(cmd)
    assert new_cmd == []


def test_get_new_command_handles_empty_script_parts():
    # Error case: script_parts is empty, should return empty list without error
    cmd = DummyCommand(
        script="choco install",
        script_parts=[]
    )
    new_cmd = get_new_command(cmd)
    assert new_cmd == []

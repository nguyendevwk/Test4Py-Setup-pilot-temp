import pytest
from thefuck.rules.choco_install import get_new_command


class DummyCommand:
    def __init__(self, script, script_parts):
        self.script = script
        self.script_parts = script_parts


def test_get_new_command_replaces_package_name():
    cmd = DummyCommand(
        script="choco install git",
        script_parts=["choco", "install", "git"]
    )
    new_cmd = get_new_command(cmd)
    assert new_cmd == "choco install git.install"
    assert isinstance(new_cmd, str)


def test_get_new_command_returns_empty_list_when_no_package():
    cmd = DummyCommand(
        script="choco install -y",
        script_parts=["choco", "install", "-y"]
    )
    new_cmd = get_new_command(cmd)
    assert new_cmd == []


def test_get_new_command_handles_multiple_parts_and_parameters():
    cmd = DummyCommand(
        script="cinst -y python",
        script_parts=["cinst", "-y", "python"]
    )
    new_cmd = get_new_command(cmd)
    assert new_cmd == "cinst -y python.install"

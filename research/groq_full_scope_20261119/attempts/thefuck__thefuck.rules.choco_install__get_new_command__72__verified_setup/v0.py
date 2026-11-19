import pytest
from thefuck.rules.choco_install import get_new_command


class DummyCommand:
    def __init__(self, script, script_parts):
        self.script = script
        self.script_parts = script_parts


def test_get_new_command_replaces_package_name(tmp_path):
    # Normal case: package name is present and should be replaced with .install
    cmd = DummyCommand(
        script="choco install git",
        script_parts=["choco", "install", "git"]
    )
    new_cmd = get_new_command(cmd)
    assert new_cmd == "choco install git.install"
    # Ensure only the first occurrence is replaced
    cmd2 = DummyCommand(
        script="choco install git --version 2.0",
        script_parts=["choco", "install", "git", "--version", "2.0"]
    )
    assert get_new_command(cmd2) == "choco install git.install --version 2.0"


def test_get_new_command_no_package_name_returns_empty_list(tmp_path):
    # Boundary case: no package name, only options
    cmd = DummyCommand(
        script="choco install --no-progress",
        script_parts=["choco", "install", "--no-progress"]
    )
    assert get_new_command(cmd) == []


def test_get_new_command_package_name_with_special_chars(tmp_path):
    # Package name containing hyphen should still be considered a package
    cmd = DummyCommand(
        script="choco install azure-cli",
        script_parts=["choco", "install", "azure-cli"]
    )
    assert get_new_command(cmd) == "choco install azure-cli.install"

    # Package name containing '=' or '/' should not be treated as a package
    cmd_eq = DummyCommand(
        script="choco install foo=bar",
        script_parts=["choco", "install", "foo=bar"]
    )
    assert get_new_command(cmd_eq) == []

    cmd_slash = DummyCommand(
        script="choco install foo/bar",
        script_parts=["choco", "install", "foo/bar"]
    )
    assert get_new_command(cmd_slash) == []

import pytest
from thefuck.rules.choco_install import get_new_command


class DummyCommand:
    def __init__(self, script: str):
        self.script = script
        # split by whitespace to mimic script_parts
        self.script_parts = script.split()


def test_get_new_command_normal():
    """When a package name is present, it should be appended with '.install'."""
    cmd = DummyCommand("choco install git")
    new_cmd = get_new_command(cmd)
    assert new_cmd == "choco install git.install"
    # Ensure only the package part was modified
    assert new_cmd.count("git.install") == 1
    assert "git" in new_cmd and ".install" in new_cmd


def test_get_new_command_with_options():
    """Options starting with '-' should be ignored; the first non-option part is the package."""
    cmd = DummyCommand("choco install -y git")
    new_cmd = get_new_command(cmd)
    assert new_cmd == "choco install -y git.install"
    # The option '-y' should remain unchanged
    assert "-y" in new_cmd
    # Only the package part should have '.install' appended
    assert new_cmd.count("git.install") == 1
    assert new_cmd.count("git") == 1  # original 'git' replaced


def test_get_new_command_no_package():
    """If no valid package name is found, an empty list should be returned."""
    cmd = DummyCommand("choco install -y")
    new_cmd = get_new_command(cmd)
    assert new_cmd == []

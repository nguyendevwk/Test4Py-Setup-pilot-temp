import pytest
from thefuck.rules.choco_install import get_new_command

class DummyCommand:
    def __init__(self, script, script_parts):
        self.script = script
        self.script_parts = script_parts

def test_get_new_command_appends_install(tmp_path):
    # Normal case: package name is present and not a flag
    cmd = DummyCommand(
        script="choco install git",
        script_parts=["choco", "install", "git"]
    )
    new_cmd = get_new_command(cmd)
    assert new_cmd == "choco install git.install"
    # Ensure the original command is unchanged
    assert cmd.script == "choco install git"

def test_get_new_command_returns_empty_when_no_package():
    # Boundary case: all parts are excluded (flags or special chars)
    cmd = DummyCommand(
        script="choco install -y --no-progress",
        script_parts=["choco", "install", "-y", "--no-progress"]
    )
    new_cmd = get_new_command(cmd)
    assert new_cmd == []

def test_get_new_command_skips_invalid_parts():
    # Error case: part contains '=' or '/' should be ignored
    cmd = DummyCommand(
        script="choco install git=1.0.0 /path/to/package",
        script_parts=["choco", "install", "git=1.0.0", "/path/to/package"]
    )
    new_cmd = get_new_command(cmd)
    assert new_cmd == []

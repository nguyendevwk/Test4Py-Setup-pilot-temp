import pytest
from thefuck.types import Command
from thefuck.exceptions import EmptyCommand

def test_command_equality_and_repr():
    cmd1 = Command("ls -l", "output1")
    cmd2 = Command("ls -l", "output1")
    cmd3 = Command("ls -a", "output1")
    assert cmd1 == cmd2
    assert cmd1 != cmd3
    assert repr(cmd1) == "Command(script=ls -l, output=output1)"

def test_script_parts_and_deprecated_properties(tmp_path):
    # Use a simple command that contains a pipe to test splitting
    cmd = Command("echo hello | grep h", "some output")
    parts = cmd.script_parts
    assert parts == ["echo", "hello", "|", "grep", "h"]
    # Access deprecated properties and ensure they return the same output
    assert cmd.stdout == "some output"
    assert cmd.stderr == "some output"

def test_from_raw_script_empty_command():
    with pytest.raises(EmptyCommand):
        Command.from_raw_script([])

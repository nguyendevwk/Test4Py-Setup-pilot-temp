import pytest
from thefuck.types import Command
from thefuck.exceptions import EmptyCommand
from thefuck.shells import shell

def test_command_equality_and_repr():
    cmd1 = Command("ls -l", "output1")
    cmd2 = Command("ls -l", "output1")
    cmd3 = Command("ls -a", "output1")
    assert cmd1 == cmd2
    assert cmd1 != cmd3
    assert repr(cmd1) == "Command(script=ls -l, output=output1)"

def test_script_parts_and_update(tmp_path):
    # create a simple script with quoted argument
    script = 'echo "hello world"'
    cmd = Command(script, "output")
    parts = cmd.script_parts
    assert parts == ['echo', 'hello world']
    # update should create a new instance with modified script
    new_cmd = cmd.update(script='echo "new"')
    assert new_cmd.script == 'echo "new"'
    assert new_cmd.output == "output"
    # original command remains unchanged
    assert cmd.script == script

def test_from_raw_script_empty_and_valid(tmp_path):
    # Empty raw_script should raise EmptyCommand
    with pytest.raises(EmptyCommand):
        Command.from_raw_script([])
    # raw_script with only whitespace should also raise
    with pytest.raises(EmptyCommand):
        Command.from_raw_script(["   "])
    # Valid raw_script: split into parts, then format and expand
    raw = ["echo", "test"]
    cmd = Command.from_raw_script(raw)
    # script should be the joined raw script
    assert cmd.script == "echo test"
    # output should not be empty (depends on shell, but should be a string)
    assert isinstance(cmd.output, str)

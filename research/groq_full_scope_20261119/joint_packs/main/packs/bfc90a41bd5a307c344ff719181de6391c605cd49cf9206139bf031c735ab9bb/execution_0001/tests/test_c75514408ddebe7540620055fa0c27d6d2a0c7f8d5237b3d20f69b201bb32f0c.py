import pytest
from thefuck.types import Command
from thefuck.exceptions import EmptyCommand
from thefuck.shells import shell

def test_script_parts_splitting_and_caching():
    # A command with quoted arguments should be split correctly
    cmd = Command('echo "Hello World" && ls -l', 'output')
    parts = cmd.script_parts
    assert parts == ['echo', 'Hello World', '&&', 'ls', '-l']
    # Accessing again should return the cached value without recomputing
    assert cmd.script_parts is parts

def test_command_equality_and_repr():
    cmd1 = Command('ls -a', 'out1')
    cmd2 = Command('ls -a', 'out1')
    cmd3 = Command('ls -l', 'out1')
    cmd4 = Command('ls -a', 'out2')
    # Equality
    assert cmd1 == cmd2
    assert cmd1 != cmd3
    assert cmd1 != cmd4
    # Representation contains script and output
    rep = repr(cmd1)
    assert 'Command(script=ls -a, output=out1)' == rep

def test_from_raw_script_empty_and_output():
    # Empty raw script should raise EmptyCommand
    with pytest.raises(EmptyCommand):
        Command.from_raw_script([])
    # Valid raw script should produce a Command with expanded script
    raw = ['echo', 'test']
    cmd = Command.from_raw_script(raw)
    # The expanded script should be a single string
    assert isinstance(cmd.script, str)
    # The output should be a string (could be empty if command prints nothing)
    assert isinstance(cmd.output, str)
    # The script should match the shell expansion of the raw parts
    expanded = shell.from_shell('echo test')
    assert cmd.script == expanded

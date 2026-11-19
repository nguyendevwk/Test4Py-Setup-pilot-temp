import os
import sys
import pytest
from thefuck.types import Command
from thefuck.exceptions import EmptyCommand
from thefuck.shells import shell
from thefuck.output_readers import get_output

def test_script_parts_splitting_and_deprecation(tmp_path):
    # Create a simple command with spaces and quotes
    cmd = Command('echo "Hello World"', 'Hello World\n')
    # script_parts should split correctly
    parts = cmd.script_parts
    assert parts == ['echo', 'Hello World']
    # Accessing deprecated properties should return the same output
    assert cmd.stdout == 'Hello World\n'
    assert cmd.stderr == 'Hello World\n'

def test_equality_and_update(tmp_path):
    cmd1 = Command('ls -l', 'output1')
    cmd2 = Command('ls -l', 'output1')
    cmd3 = Command('ls -a', 'output1')
    # Equality checks
    assert cmd1 == cmd2
    assert cmd1 != cmd3
    # Update should create a new instance with modified fields
    cmd4 = cmd1.update(script='ls -a')
    assert cmd4.script == 'ls -a'
    assert cmd4.output == 'output1'
    # Original remains unchanged
    assert cmd1.script == 'ls -l'

def test_from_raw_script_empty_and_valid(tmp_path):
    # Empty raw script should raise EmptyCommand
    with pytest.raises(EmptyCommand):
        Command.from_raw_script([])
    # Valid raw script should produce a Command with expanded script
    raw = ['echo', 'test']
    cmd = Command.from_raw_script(raw)
    # The expanded script should be a single string
    assert isinstance(cmd.script, str)
    # The output should be captured by get_output
    expected_output = get_output(cmd.script, cmd.script)
    assert cmd.output == expected_output

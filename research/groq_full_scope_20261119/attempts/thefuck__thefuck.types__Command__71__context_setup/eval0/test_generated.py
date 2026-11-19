import os
import pytest
from thefuck.types import Command
from thefuck.exceptions import EmptyCommand
from thefuck.shells import shell

def test_script_parts_splitting(tmp_path):
    # Create a simple command with quoted arguments
    cmd = Command('echo "Hello World" && ls -l', '')
    parts = cmd.script_parts
    # shell.split_command should split into ['echo', 'Hello World', '&&', 'ls', '-l']
    assert parts == ['echo', 'Hello World', '&&', 'ls', '-l']
    # Repeated access should not recompute
    parts_again = cmd.script_parts
    assert parts_again is parts

def test_command_equality_and_repr():
    cmd1 = Command('ls', 'output')
    cmd2 = Command('ls', 'output')
    cmd3 = Command('ls', 'different')
    # Equality based on script and output
    assert cmd1 == cmd2
    assert cmd1 != cmd3
    # __repr__ should include script and output
    rep = repr(cmd1)
    assert 'Command(script=ls' in rep
    assert 'output=output' in rep

def test_from_raw_script_empty_and_output(tmp_path):
    # Empty raw script should raise EmptyCommand
    with pytest.raises(EmptyCommand):
        Command.from_raw_script([])
    # Valid raw script: use a temporary file to avoid side effects
    tmp_file = tmp_path / "test.txt"
    tmp_file.write_text("test")
    raw = ['cat', str(tmp_file)]
    cmd = Command.from_raw_script(raw)
    # The script should be expanded (no shell expansion needed)
    assert cmd.script == f'cat {tmp_file}'
    # Output should be the file content
    assert cmd.output == "test"

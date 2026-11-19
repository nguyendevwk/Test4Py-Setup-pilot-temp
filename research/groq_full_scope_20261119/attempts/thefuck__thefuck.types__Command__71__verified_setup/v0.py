import os
import pytest
from thefuck.types import Command
from thefuck.exceptions import EmptyCommand
from thefuck.shells import shell

def test_script_parts_splitting(tmp_path):
    # Create a simple script with quoted arguments
    script = 'echo "Hello World" && ls -l'
    cmd = Command(script, "output")
    parts = cmd.script_parts
    # shell.split_command should split into ['echo', 'Hello World', '&&', 'ls', '-l']
    assert parts == ['echo', 'Hello World', '&&', 'ls', '-l']

def test_command_equality_and_repr():
    cmd1 = Command("ls -a", "output")
    cmd2 = Command("ls -a", "output")
    cmd3 = Command("ls -l", "output")
    # Equality
    assert cmd1 == cmd2
    assert cmd1 != cmd3
    # Representation contains script and output
    rep = repr(cmd1)
    assert "ls -a" in rep
    assert "output" in rep

def test_from_raw_script_empty_and_output(tmp_path):
    # Empty raw script should raise EmptyCommand
    with pytest.raises(EmptyCommand):
        Command.from_raw_script([])
    # Valid raw script: use a temporary file to avoid side effects
    tmp_file = tmp_path / "test.txt"
    tmp_file.write_text("content")
    raw = ['cat', str(tmp_file)]
    cmd = Command.from_raw_script(raw)
    # The expanded script should be the same as raw joined
    assert cmd.script == f'cat {tmp_file}'
    # Output should be the file content
    assert cmd.output == "content"

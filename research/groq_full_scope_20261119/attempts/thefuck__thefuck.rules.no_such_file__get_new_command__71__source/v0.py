import re
import pytest
from thefuck.rules import no_such_file

class DummyCommand:
    def __init__(self, output, script):
        self.output = output
        self.script = script

def test_get_new_command_creates_mkdir_for_existing_file(tmp_path):
    # Arrange: create a command whose output contains a file path
    file_path = str(tmp_path / "subdir" / "file.txt")
    output = f"Error: No such file or directory: '{file_path}'"
    cmd = DummyCommand(output=output, script="cat file.txt")
    # Act
    new_cmd = no_such_file.get_new_command(cmd)
    # Assert: the new command should create the directory and then run the original script
    expected_dir = str(tmp_path / "subdir")
    assert new_cmd.startswith("mkdir -p")
    assert expected_dir in new_cmd
    assert cmd.script in new_cmd

def test_get_new_command_handles_root_file(tmp_path):
    # Arrange: file at root of tmp_path
    file_path = str(tmp_path / "rootfile.txt")
    output = f"Error: No such file or directory: '{file_path}'"
    cmd = DummyCommand(output=output, script="cat rootfile.txt")
    # Act
    new_cmd = no_such_file.get_new_command(cmd)
    # Assert: directory part should be empty string, but mkdir -p '' is acceptable
    assert new_cmd.startswith("mkdir -p")
    # The directory part before the last slash is empty, so the command should still contain the script
    assert cmd.script in new_cmd

def test_get_new_command_returns_none_when_no_match(tmp_path):
    # Arrange: output that does not contain any file path
    output = "Error: Something went wrong"
    cmd = DummyCommand(output=output, script="cat missing.txt")
    # Act
    new_cmd = no_such_file.get_new_command(cmd)
    # Assert: no command should be suggested
    assert new_cmd is None

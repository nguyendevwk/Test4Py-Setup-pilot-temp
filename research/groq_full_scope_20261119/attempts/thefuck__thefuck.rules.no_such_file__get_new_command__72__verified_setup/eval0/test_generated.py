import re
import pytest
from thefuck.rules.no_such_file import get_new_command
from thefuck.shells import shell

class DummyCommand:
    def __init__(self, output, script):
        self.output = output
        self.script = script

def test_get_new_command_creates_mkdir_and_runs_script(tmp_path):
    # Create a temporary file path to simulate a missing file
    temp_file = tmp_path / "missing.txt"
    # Simulate the error message that thefuck would receive
    output = f"cat: {temp_file}: No such file or directory"
    command = DummyCommand(output=output, script=f"cat {temp_file}")
    # Call the function under test
    result = get_new_command(command)
    # The expected directory is the parent of the missing file
    expected_dir = str(temp_file.parent)
    # shell.and_('mkdir -p {}', '{}') should produce a string with two placeholders
    expected = f"mkdir -p {expected_dir} && cat {temp_file}"
    assert result == expected

def test_get_new_command_returns_none_when_no_match(tmp_path):
    # Simulate an error message that does not contain a file path
    output = "cat: No such file or directory"
    command = DummyCommand(output=output, script="cat missing.txt")
    # The function should return None when no file path is found
    assert get_new_command(command) is None

def test_get_new_command_uses_first_match(tmp_path):
    # Create two temporary file paths
    file1 = tmp_path / "first.txt"
    file2 = tmp_path / "second.txt"
    # Simulate an error message containing both paths
    output = f"cat: {file1}: No such file or directory\ncat: {file2}: No such file or directory"
    command = DummyCommand(output=output, script=f"cat {file1}")
    # The function should use the first match (file1)
    result = get_new_command(command)
    expected_dir = str(file1.parent)
    expected = f"mkdir -p {expected_dir} && cat {file1}"
    assert result == expected

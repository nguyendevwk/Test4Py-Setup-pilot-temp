import re
import pytest
from thefuck.rules.no_such_file import get_new_command, patterns
from thefuck.shells import shell

class DummyCommand:
    def __init__(self, output, script):
        self.output = output
        self.script = script

def test_get_new_command_creates_mkdir_and_runs_script(tmp_path):
    # Create a temporary file path to simulate a missing file
    file_path = tmp_path / "subdir" / "missing.txt"
    # Ensure the directory part exists in the output string
    output = f"cat: {file_path}: No such file or directory"
    cmd = DummyCommand(output=output, script="cat missing.txt")
    new_cmd = get_new_command(cmd)
    # The new command should create the parent directory and then run the original script
    expected_dir = str(file_path.parent)
    assert new_cmd == f"mkdir -p {expected_dir} && {cmd.script}"

def test_get_new_command_returns_none_when_no_match(tmp_path):
    # Output that does not contain any file path
    output = "cat: No such file or directory"
    cmd = DummyCommand(output=output, script="cat missing.txt")
    assert get_new_command(cmd) is None

def test_get_new_command_uses_first_match_when_multiple(tmp_path):
    # Output containing two file paths; the first should be used
    file1 = tmp_path / "a.txt"
    file2 = tmp_path / "b.txt"
    output = f"cat: {file1}: No such file or directory\ncat: {file2}: No such file or directory"
    cmd = DummyCommand(output=output, script="cat a.txt")
    new_cmd = get_new_command(cmd)
    expected_dir = str(file1.parent)
    assert new_cmd == f"mkdir -p {expected_dir} && {cmd.script}"

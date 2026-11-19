import re
import pytest
from thefuck.rules.no_such_file import get_new_command, patterns
from thefuck.shells import shell

# Helper command object mimicking the real Command
class DummyCommand:
    def __init__(self, script, output):
        self.script = script
        self.output = output

def test_get_new_command_creates_mkdir_and_uses_original_script(tmp_path):
    # Arrange: create a file path that does not exist
    missing_file = tmp_path / "missing.txt"
    # Simulate an error message from mv
    output = f"mv: cannot move 'source.txt' to '{missing_file}': No such file or directory"
    cmd = DummyCommand(script="mv source.txt missing.txt", output=output)

    # Act
    new_cmd = get_new_command(cmd)

    # Assert
    expected_dir = str(tmp_path)
    assert new_cmd == f"mkdir -p {expected_dir} && mv source.txt missing.txt"

def test_get_new_command_handles_root_directory(tmp_path):
    # Arrange: missing file at root
    missing_file = "/root_missing.txt"
    output = f"cp: cannot create regular file '{missing_file}': No such file or directory"
    cmd = DummyCommand(script="cp source.txt /root_missing.txt", output=output)

    # Act
    new_cmd = get_new_command(cmd)

    # Assert: dir part before last slash is empty string, so mkdir -p '' is harmless
    assert new_cmd == "mkdir -p  && cp source.txt /root_missing.txt"

def test_get_new_command_returns_none_when_no_pattern_matches(tmp_path):
    # Arrange: output that does not match any pattern
    output = "some unrelated error message"
    cmd = DummyCommand(script="echo hello", output=output)

    # Act
    new_cmd = get_new_command(cmd)

    # Assert
    assert new_cmd is None

import re
import pytest
from thefuck.rules.no_such_file import get_new_command, patterns
from thefuck.shells import shell

class DummyCommand:
    def __init__(self, output, script):
        self.output = output
        self.script = script

def test_get_new_command_normal(tmp_path):
    # Monkey‑patch patterns to match a quoted file path
    patterns[:] = [r"'([^']+)'"]
    cmd = DummyCommand(
        output="bash: No such file or directory: 'src/main.py'",
        script="python src/main.py"
    )
    expected_dir = "src"
    expected = f"mkdir -p {expected_dir} && mkdir -p src/main.py"
    assert get_new_command(cmd) == expected

def test_get_new_command_boundary(tmp_path):
    # Pattern matches a quoted file path without a slash
    patterns[:] = [r"'([^']+)'"]
    cmd = DummyCommand(
        output="bash: No such file or directory: 'file.txt'",
        script="cat file.txt"
    )
    # dir will be everything before the last slash; since there is none,
    # rfind returns -1 and dir becomes file[:-1] (all but last char)
    expected_dir = "file"
    expected = f"mkdir -p {expected_dir} && mkdir -p file.txt"
    assert get_new_command(cmd) == expected

def test_get_new_command_no_match(tmp_path):
    # Pattern that does not match the output
    patterns[:] = [r"'([^']+)'"]
    cmd = DummyCommand(
        output="bash: command not found: ls",
        script="ls -l"
    )
    assert get_new_command(cmd) is None

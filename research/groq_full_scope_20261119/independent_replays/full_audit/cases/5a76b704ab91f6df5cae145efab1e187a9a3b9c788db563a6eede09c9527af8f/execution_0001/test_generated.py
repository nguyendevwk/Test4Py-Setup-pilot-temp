import re
import pytest
from thefuck.rules.no_such_file import match, patterns

class DummyCommand:
    def __init__(self, output):
        self.output = output

def test_match_detects_mv_no_such_file():
    """match should return True when mv reports a missing file."""
    cmd = DummyCommand(
        "mv: cannot move 'foo.txt' to 'bar.txt': No such file or directory"
    )
    assert match(cmd) is True

def test_match_detects_cp_not_a_directory():
    """match should return True when cp reports a target that is not a directory."""
    cmd = DummyCommand(
        "cp: cannot create regular file 'baz.txt': Not a directory"
    )
    assert match(cmd) is True

def test_match_returns_false_for_unrelated_output():
    """match should return False when the output does not match any pattern."""
    cmd = DummyCommand(
        "some unrelated error message that should not match any pattern"
    )
    assert match(cmd) is False

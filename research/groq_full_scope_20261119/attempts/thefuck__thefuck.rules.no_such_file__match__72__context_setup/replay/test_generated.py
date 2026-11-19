import re
import types
import pytest
from thefuck.rules.no_such_file import match, patterns

def make_command(output: str):
    """Create a simple command object with an `output` attribute."""
    cmd = types.SimpleNamespace()
    cmd.output = output
    return cmd

def test_match_mv_no_such_file():
    """`match` should return True for a mv error about a missing file."""
    output = "mv: cannot move 'foo.txt' to 'bar.txt': No such file or directory"
    cmd = make_command(output)
    assert match(cmd) is True

def test_match_boundary_not_a_directory():
    """`match` should return True for a cp error when destination is not a directory."""
    output = "cp: cannot create regular file 'baz.txt': Not a directory"
    cmd = make_command(output)
    assert match(cmd) is True

def test_match_no_match():
    """`match` should return False when the output does not match any pattern."""
    output = "some unrelated error message"
    cmd = make_command(output)
    assert match(cmd) is False

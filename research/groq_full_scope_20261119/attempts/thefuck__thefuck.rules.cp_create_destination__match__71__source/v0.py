import pytest
from thefuck.rules.cp_create_destination import match

class DummyCommand:
    def __init__(self, output: str):
        self.output = output

def test_match_no_such_file_or_directory():
    """Should match when output contains the phrase 'No such file or directory'."""
    cmd = DummyCommand("cp: No such file or directory")
    assert match(cmd) is True

def test_match_directory_does_not_exist():
    """Should match when output starts with 'cp: directory' and ends with 'does not exist'."""
    cmd = DummyCommand("cp: directory /tmp/foo does not exist")
    assert match(cmd) is True

def test_match_no_match_other_output():
    """Should not match when output does not contain any of the expected patterns."""
    cmd = DummyCommand("cp: cannot stat 'file': No such file or directory")
    assert match(cmd) is False

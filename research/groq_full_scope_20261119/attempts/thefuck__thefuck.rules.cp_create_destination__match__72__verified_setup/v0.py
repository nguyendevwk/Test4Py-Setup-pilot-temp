import pytest
from thefuck.rules.cp_create_destination import match

class DummyCommand:
    def __init__(self, output: str):
        self.output = output

def test_match_detects_no_such_file_or_directory():
    cmd = DummyCommand("No such file or directory: 'file.txt'")
    assert match(cmd) is True

def test_match_detects_cp_directory_error_with_trailing_newline():
    cmd = DummyCommand("cp: directory 'src' does not exist\n")
    assert match(cmd) is True

def test_match_returns_false_for_unrelated_error():
    cmd = DummyCommand("Some other error message")
    assert match(cmd) is False

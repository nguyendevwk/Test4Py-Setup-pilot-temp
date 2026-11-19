import pytest
from thefuck.rules.git_diff_no_index import match

class DummyCommand:
    def __init__(self, script, script_parts):
        self.script = script
        self.script_parts = script_parts

def test_match_true_when_diff_and_two_files_and_no_no_index():
    cmd = DummyCommand(
        script="git diff file1.txt file2.txt",
        script_parts=["git", "diff", "file1.txt", "file2.txt"]
    )
    assert match(cmd) is True

def test_match_false_when_more_than_two_files():
    cmd = DummyCommand(
        script="git diff file1.txt file2.txt file3.txt",
        script_parts=["git", "diff", "file1.txt", "file2.txt", "file3.txt"]
    )
    assert match(cmd) is False

def test_match_false_when_no_diff_or_has_no_index():
    cmd1 = DummyCommand(
        script="git status",
        script_parts=["git", "status"]
    )
    cmd2 = DummyCommand(
        script="git diff --no-index file1.txt file2.txt",
        script_parts=["git", "diff", "--no-index", "file1.txt", "file2.txt"]
    )
    assert match(cmd1) is False
    assert match(cmd2) is False

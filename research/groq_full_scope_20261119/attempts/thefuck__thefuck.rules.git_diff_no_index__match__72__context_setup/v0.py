import pytest
from thefuck.rules.git_diff_no_index import match

class DummyCommand:
    def __init__(self, script, script_parts):
        self.script = script
        self.script_parts = script_parts

def test_match_successful_diff_no_index(tmp_path):
    # Two file arguments, no --no-index flag, and 'diff' present
    cmd = DummyCommand(
        script="git diff file1.txt file2.txt",
        script_parts=["git", "diff", "file1.txt", "file2.txt"]
    )
    assert match(cmd) is True

def test_match_failure_due_to_missing_file(tmp_path):
    # Only one file argument, should not match
    cmd = DummyCommand(
        script="git diff file1.txt",
        script_parts=["git", "diff", "file1.txt"]
    )
    assert match(cmd) is False

def test_match_failure_due_to_no_index_flag(tmp_path):
    # Contains --no-index flag, should not match
    cmd = DummyCommand(
        script="git diff --no-index file1.txt file2.txt",
        script_parts=["git", "diff", "--no-index", "file1.txt", "file2.txt"]
    )
    assert match(cmd) is False

import pytest
from thefuck.rules.git_diff_no_index import match

class DummyCommand:
    def __init__(self, script, script_parts):
        self.script = script
        self.script_parts = script_parts

def test_match_successful_diff_no_index_two_files():
    """When the command contains 'diff', no '--no-index', and exactly two file arguments."""
    cmd = DummyCommand(
        script="git diff file1.txt file2.txt",
        script_parts=["git", "diff", "file1.txt", "file2.txt"]
    )
    assert match(cmd) is True

def test_match_failure_due_to_extra_file_argument():
    """When more than two file arguments are present, match should return False."""
    cmd = DummyCommand(
        script="git diff file1.txt file2.txt file3.txt",
        script_parts=["git", "diff", "file1.txt", "file2.txt", "file3.txt"]
    )
    assert match(cmd) is False

def test_match_failure_due_to_no_diff_or_no_index_flag():
    """When the command lacks 'diff' or includes '--no-index', match should return False."""
    # Missing 'diff'
    cmd1 = DummyCommand(
        script="git status file1.txt file2.txt",
        script_parts=["git", "status", "file1.txt", "file2.txt"]
    )
    assert match(cmd1) is False

    # Contains '--no-index'
    cmd2 = DummyCommand(
        script="git diff --no-index file1.txt file2.txt",
        script_parts=["git", "diff", "--no-index", "file1.txt", "file2.txt"]
    )
    assert match(cmd2) is False

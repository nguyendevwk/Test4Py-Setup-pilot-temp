import pytest
from thefuck.rules.git_diff_no_index import match


class DummyCommand:
    def __init__(self, script, script_parts):
        self.script = script
        self.script_parts = script_parts


def test_match_true_when_diff_and_two_files_and_no_no_index(tmp_path):
    """The rule should match when the command contains 'diff', two file arguments,
    and does not contain '--no-index'."""
    cmd = DummyCommand(
        script="git diff file1.txt file2.txt",
        script_parts=["git", "diff", "file1.txt", "file2.txt"]
    )
    assert match(cmd) is True


def test_match_false_when_only_one_file(tmp_path):
    """The rule should not match when only one file argument is provided."""
    cmd = DummyCommand(
        script="git diff file1.txt",
        script_parts=["git", "diff", "file1.txt"]
    )
    assert match(cmd) is False


def test_match_false_when_no_diff_in_script(tmp_path):
    """The rule should not match when the script does not contain the word 'diff'."""
    cmd = DummyCommand(
        script="git status file1.txt file2.txt",
        script_parts=["git", "status", "file1.txt", "file2.txt"]
    )
    assert match(cmd) is False

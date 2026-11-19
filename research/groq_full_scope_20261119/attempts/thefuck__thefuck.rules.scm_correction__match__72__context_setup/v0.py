import pytest
from pathlib import Path
from thefuck.rules.scm_correction import match, _get_actual_scm, wrong_scm_patterns, path_to_scm


class DummyCommand:
    def __init__(self, script_parts, output):
        self.script_parts = script_parts
        self.output = output


def test_match_success(tmp_path):
    # Create a git repository directory
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    # Command uses git and output contains the git error pattern
    cmd = DummyCommand(script_parts=["git"], output="fatal: Not a git repository")
    assert match(cmd) is True
    # Ensure _get_actual_scm returns 'git'
    assert _get_actual_scm() == "git"


def test_match_no_pattern(tmp_path):
    # Create a git repository directory
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    # Command uses git but output does not contain the pattern
    cmd = DummyCommand(script_parts=["git"], output="some other error")
    assert match(cmd) is False
    # _get_actual_scm still returns 'git'
    assert _get_actual_scm() == "git"


def test_match_no_repository(tmp_path):
    # No .git or .hg directory present
    cmd = DummyCommand(script_parts=["git"], output="fatal: Not a git repository")
    # Since no repository directory exists, match should be False
    assert match(cmd) is False
    # _get_actual_scm should return None
    assert _get_actual_scm() is None

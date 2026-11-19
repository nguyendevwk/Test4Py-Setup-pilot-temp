import pytest
from pathlib import Path
from thefuck.rules.scm_correction import match, _get_actual_scm, wrong_scm_patterns, path_to_scm

class DummyCommand:
    def __init__(self, script_parts, output):
        self.script_parts = script_parts
        self.output = output

def test_match_git_repository(tmp_path):
    # Create a .git directory to simulate a git repo
    (tmp_path / ".git").mkdir()
    # Change working directory to tmp_path so Path.is_dir finds the .git folder
    cwd = Path.cwd()
    try:
        Path(tmp_path).cwd()
    except AttributeError:
        # For Python <3.11, manually change cwd
        import os
        os.chdir(tmp_path)
    # Prepare command that should match
    cmd = DummyCommand(script_parts=["git"], output="fatal: Not a git repository")
    # Ensure _get_actual_scm returns 'git'
    assert _get_actual_scm() == "git"
    # match should return True
    assert match(cmd) is True

def test_match_no_repository(tmp_path):
    # No .git or .hg directory present
    # Prepare command that would match if a repo existed
    cmd = DummyCommand(script_parts=["git"], output="fatal: Not a git repository")
    # _get_actual_scm should return None
    assert _get_actual_scm() is None
    # match should return False because no actual scm directory
    assert match(cmd) is False

def test_match_hg_repository(tmp_path):
    # Create a .hg directory to simulate a hg repo
    (tmp_path / ".hg").mkdir()
    cwd = Path.cwd()
    try:
        Path(tmp_path).cwd()
    except AttributeError:
        import os
        os.chdir(tmp_path)
    # Prepare command that should match for hg
    cmd = DummyCommand(script_parts=["hg"], output="abort: no repository found")
    # Ensure _get_actual_scm returns 'hg'
    assert _get_actual_scm() == "hg"
    # match should return True
    assert match(cmd) is True

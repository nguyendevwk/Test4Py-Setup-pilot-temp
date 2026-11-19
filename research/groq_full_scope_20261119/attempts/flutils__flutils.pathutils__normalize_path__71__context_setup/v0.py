import os
import sys
import pytest
from pathlib import Path
from flutils.pathutils import normalize_path

def test_normalize_with_home_and_env(tmp_path):
    # Set up environment variable and home directory
    os.environ["TEST_VAR"] = "subdir"
    # Create a temporary directory to act as the user's home
    home_dir = tmp_path / "home"
    home_dir.mkdir()
    # Monkeypatch getpass.getuser to return a user whose home is home_dir
    original_getuser = os.getlogin if hasattr(os, "getlogin") else None
    try:
        os.getlogin = lambda: "dummy_user"
        # Create a dummy user entry in pwd module
        import pwd
        pwd.getpwnam = lambda u: type("pwd", (), {"pw_dir": str(home_dir)})()
        # Path containing ~ and env var
        input_path = "~/folder/${TEST_VAR}/file.txt"
        result = normalize_path(input_path)
        expected = Path(home_dir, "folder", "subdir", "file.txt")
        assert result == expected
    finally:
        if original_getuser:
            os.getlogin = original_getuser
        del os.environ["TEST_VAR"]

def test_normalize_relative_path(tmp_path):
    # Create a relative path that includes up-level references
    rel_path = Path("a") / "b" / ".." / "c" / "."
    # Change current working directory to tmp_path
    cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        result = normalize_path(rel_path)
        expected = tmp_path / "a" / "c"
        assert result == expected
    finally:
        os.chdir(cwd)

def test_normalize_invalid_input():
    with pytest.raises(TypeError):
        normalize_path(None)

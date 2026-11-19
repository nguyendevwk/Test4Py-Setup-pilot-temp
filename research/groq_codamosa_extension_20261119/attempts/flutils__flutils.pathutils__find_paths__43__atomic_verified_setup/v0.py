import os
import sys
import pytest
from pathlib import Path
from flutils.pathutils import find_paths

def test_find_paths_basic(tmp_path):
    # Create a simple directory structure
    (tmp_path / "file1.txt").write_text("a")
    (tmp_path / "file2.log").write_text("b")
    (tmp_path / "subdir").mkdir()
    (tmp_path / "subdir" / "file3.txt").write_text("c")

    # Use glob pattern to find all .txt files
    pattern = str(tmp_path / "*.txt")
    result = list(find_paths(pattern))

    # Assert that the returned paths match the expected files
    expected = {tmp_path / "file1.txt"}
    assert set(result) == expected

    # Now include subdirectory files
    pattern = str(tmp_path / "**/*.txt")
    result = list(find_paths(pattern))
    expected = {tmp_path / "file1.txt", tmp_path / "subdir" / "file3.txt"}
    assert set(result) == expected

def test_find_paths_tilde(tmp_path, monkeypatch):
    # Create a temporary home directory and a file inside
    home = tmp_path / "home"
    home.mkdir()
    user_dir = home / "test_user"
    user_dir.mkdir()
    file_path = user_dir / "tmp" / "file_one"
    file_path.parent.mkdir(parents=True)
    file_path.write_text("content")

    # Monkeypatch getpass.getuser to return 'test_user'
    monkeypatch.setattr("getpass.getuser", lambda: "test_user")

    # Monkeypatch os.path.expanduser to use our fake home
    monkeypatch.setattr("os.path.expanduser", lambda p: str(home / p.lstrip("~")))

    # Use a pattern with ~ expansion
    pattern = "~/tmp/*"
    result = list(find_paths(pattern))

    # The result should contain the file we created
    assert len(result) == 1
    assert result[0] == file_path

def test_find_paths_invalid_type():
    # Passing an integer should raise a TypeError due to normalize_path
    with pytest.raises(TypeError):
        list(find_paths(1))

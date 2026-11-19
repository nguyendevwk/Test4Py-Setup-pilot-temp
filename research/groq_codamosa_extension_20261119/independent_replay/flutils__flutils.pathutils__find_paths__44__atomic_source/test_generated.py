import os
import getpass
import pytest
from pathlib import Path
from flutils.pathutils import find_paths, normalize_path

def test_find_paths_with_glob(tmp_path):
    # Create a directory structure
    (tmp_path / "dir1").mkdir()
    (tmp_path / "dir2").mkdir()
    (tmp_path / "file1.txt").write_text("a")
    (tmp_path / "file2.log").write_text("b")
    # Use glob pattern to find all .txt files
    pattern = tmp_path / "*.txt"
    found = list(find_paths(pattern))
    assert len(found) == 1
    assert found[0].name == "file1.txt"
    assert found[0].is_file()

def test_find_paths_with_home_expansion(tmp_path, monkeypatch):
    # Monkeypatch HOME to point to tmp_path
    monkeypatch.setenv("HOME", str(tmp_path))
    # Create a file in the home directory
    home_file = tmp_path / "home_file.txt"
    home_file.write_text("home")
    # Use tilde expansion in pattern
    pattern = "~/home_file.txt"
    found = list(find_paths(pattern))
    assert len(found) == 1
    assert found[0] == home_file
    assert found[0].is_file()

def test_find_paths_with_bytes_pattern(tmp_path):
    # Create a file
    file_path = tmp_path / "bytes_file.txt"
    file_path.write_text("bytes")
    # Pass a bytes pattern
    pattern_bytes = str(file_path).encode()
    found = list(find_paths(pattern_bytes))
    assert len(found) == 1
    assert found[0] == file_path
    assert found[0].is_file()

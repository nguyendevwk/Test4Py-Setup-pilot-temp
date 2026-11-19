import os
import sys
import pytest
from pathlib import Path
from flutils.pathutils import find_paths, normalize_path

def test_find_paths_with_glob(tmp_path):
    # Setup: create a directory structure with files and subdirectories
    (tmp_path / "file_one").write_text("one")
    (tmp_path / "file_two").write_text("two")
    (tmp_path / "dir_one").mkdir()
    (tmp_path / "dir_one" / "inner.txt").write_text("inner")

    # Use a glob pattern that matches files only
    pattern = str(tmp_path / "*")
    # Resolve pattern to absolute path for comparison
    expected = sorted([p for p in tmp_path.iterdir() if p.is_file()])

    # Call find_paths and collect results
    result = sorted(find_paths(pattern))
    assert result == expected, f"Expected {expected}, got {result}"

def test_find_paths_no_matches(tmp_path):
    # Setup: create a file that does not match the pattern
    (tmp_path / "keep.txt").write_text("keep")
    # Pattern that matches nothing
    pattern = str(tmp_path / "*.nonexistent")
    # find_paths should yield nothing
    result = list(find_paths(pattern))
    assert result == [], f"Expected empty list, got {result}"

def test_find_paths_with_home_expansion(tmp_path, monkeypatch):
    # Create a temporary home directory and a file inside it
    home_dir = tmp_path / "home_user"
    home_dir.mkdir()
    (home_dir / "home_file.txt").write_text("home")
    # Monkeypatch getpass.getuser to return a fake username
    monkeypatch.setattr("getpass.getuser", lambda: "test_user")
    # Monkeypatch os.path.expanduser to use our fake home directory
    original_expanduser = os.path.expanduser
    monkeypatch.setattr(
        os.path,
        "expanduser",
        lambda p: p.replace("~", str(home_dir))
    )
    # Pattern using ~ to refer to home
    pattern = "~/home_file.txt"
    # Normalize path should resolve to the file in our fake home
    normalized = normalize_path(pattern)
    assert normalized == home_dir / "home_file.txt"
    # find_paths should yield that file
    result = list(find_paths(pattern))
    assert result == [normalized], f"Expected {[normalized]}, got {result}"

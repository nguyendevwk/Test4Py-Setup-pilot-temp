import os
import sys
import pytest
from pathlib import Path
from flutils.pathutils import find_paths, normalize_path

def test_find_paths_normal(tmp_path):
    # Setup: create a directory with files and subdirectory
    (tmp_path / "file_one").write_text("a")
    (tmp_path / "file_two").write_text("b")
    (tmp_path / "dir_one").mkdir()
    (tmp_path / "dir_one" / "inner.txt").write_text("c")

    # Use a glob pattern that matches files only
    pattern = str(tmp_path / "*")
    # Resolve pattern to absolute path for comparison
    expected = sorted([p for p in tmp_path.iterdir() if p.is_file()])

    # Run find_paths and collect results
    result = sorted(find_paths(pattern))
    assert result == expected, f"Expected {expected}, got {result}"

def test_find_paths_no_match(tmp_path):
    # Setup: create a file that does not match the pattern
    (tmp_path / "keep.txt").write_text("data")

    # Pattern that matches nothing
    pattern = str(tmp_path / "nonexistent_*")
    # find_paths should yield nothing
    result = list(find_paths(pattern))
    assert result == [], f"Expected empty list, got {result}"

def test_find_paths_invalid_pattern(tmp_path):
    # Setup: create a simple file
    (tmp_path / "file.txt").write_text("content")

    # Use an invalid glob pattern that Path.glob will reject
    # For example, unmatched bracket
    pattern = str(tmp_path / "[invalid")
    # normalize_path will not raise, but Path.glob will raise ValueError
    with pytest.raises(ValueError):
        list(find_paths(pattern))

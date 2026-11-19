import os
import sys
import pytest
from pathlib import Path
from flutils.pathutils import find_paths, normalize_path

# Helper to create a file or directory
def _create(path: Path, is_dir: bool = False) -> None:
    if is_dir:
        path.mkdir(parents=True, exist_ok=True)
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()

def test_find_paths_basic(tmp_path: Path):
    """Verify that find_paths returns all matching files and directories."""
    # Setup: create a directory structure
    dir_a = tmp_path / "dir_a"
    dir_b = tmp_path / "dir_b"
    file_a = tmp_path / "file_a.txt"
    file_b = tmp_path / "file_b.log"
    _create(dir_a, is_dir=True)
    _create(dir_b, is_dir=True)
    _create(file_a)
    _create(file_b)

    # Use a glob pattern to match all .txt files
    pattern = str(tmp_path / "*.txt")
    result = list(find_paths(pattern))

    # Expect only file_a.txt to be returned
    assert len(result) == 1
    assert result[0] == file_a
    assert isinstance(result[0], Path)

def test_find_paths_no_matches(tmp_path: Path):
    """Verify that find_paths yields nothing when the pattern matches no paths."""
    # Setup: create a file that does not match the pattern
    _create(tmp_path / "example.txt")

    # Pattern that matches .log files, which are absent
    pattern = str(tmp_path / "*.log")
    result = list(find_paths(pattern))

    # Expect an empty list
    assert result == []

def test_find_paths_invalid_pattern():
    """Verify that passing an unsupported type raises a TypeError."""
    # Passing None should raise a TypeError because normalize_path expects a string, bytes, or Path
    with pytest.raises(TypeError):
        list(find_paths(None))

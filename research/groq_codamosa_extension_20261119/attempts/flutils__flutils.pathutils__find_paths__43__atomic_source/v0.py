import os
import sys
import pytest
from pathlib import Path
from flutils.pathutils import find_paths

@pytest.mark.parametrize("pattern,expected_names", [
    ("sub/*.txt", ["file1.txt", "file2.txt"]),
    ("sub/dir/*.md", ["doc.md"]),
])
def test_find_paths_basic(tmp_path, pattern, expected_names):
    # Setup directory structure
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "file1.txt").write_text("a")
    (sub / "file2.txt").write_text("b")
    (sub / "file3.py").write_text("c")
    dir_sub = sub / "dir"
    dir_sub.mkdir()
    (dir_sub / "doc.md").write_text("d")

    # Resolve pattern relative to tmp_path
    resolved_pattern = tmp_path / pattern
    # Call find_paths
    result = list(find_paths(resolved_pattern))
    # Assert that only expected files are returned
    assert sorted(p.name for p in result) == sorted(expected_names)
    # Assert that returned objects are Path instances
    assert all(isinstance(p, Path) for p in result)

def test_find_paths_no_matches(tmp_path):
    # Create a directory with no matching files
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    # Pattern that matches nothing
    pattern = empty_dir / "*.nonexistent"
    # find_paths should yield nothing
    result = list(find_paths(pattern))
    assert result == []

def test_find_paths_invalid_input(tmp_path):
    # Passing an integer should raise a TypeError
    with pytest.raises(TypeError):
        list(find_paths(123))

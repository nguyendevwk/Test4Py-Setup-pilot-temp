import os
import sys
import pytest
from pathlib import Path
from flutils.pathutils import find_paths, normalize_path

def test_find_paths_expands_user_and_glob(tmp_path):
    # Create a directory structure under the user's home
    home = Path.home()
    target_dir = home / "tmp_test_find"
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / "file1.txt").write_text("a")
    (target_dir / "file2.txt").write_text("b")
    # Use a glob pattern with ~ expansion
    pattern = f"~{target_dir.relative_to(home)}/file*.txt"
    # Ensure the pattern is resolved to the correct absolute path
    resolved = normalize_path(pattern)
    assert resolved.is_absolute()
    # Collect results from find_paths
    results = list(find_paths(pattern))
    # Expect both files to be found
    expected = {target_dir / "file1.txt", target_dir / "file2.txt"}
    assert set(results) == expected

def test_find_paths_no_matches(tmp_path):
    # Create a temporary directory with no matching files
    empty_dir = tmp_path / "empty_dir"
    empty_dir.mkdir()
    # Pattern that matches nothing
    pattern = str(empty_dir / "nonexistent_*.txt")
    # find_paths should yield nothing
    results = list(find_paths(pattern))
    assert results == []

def test_find_paths_invalid_pattern(tmp_path):
    # Create a directory with a file that has a name that could be interpreted as a pattern
    dir_with_file = tmp_path / "dir_with_file"
    dir_with_file.mkdir()
    (dir_with_file / "file[1].txt").write_text("content")
    # Use a pattern that is syntactically invalid for glob (e.g., unmatched bracket)
    invalid_pattern = str(dir_with_file / "file[.txt")
    # Path.glob will raise a ValueError for an invalid pattern
    with pytest.raises(ValueError):
        list(find_paths(invalid_pattern))

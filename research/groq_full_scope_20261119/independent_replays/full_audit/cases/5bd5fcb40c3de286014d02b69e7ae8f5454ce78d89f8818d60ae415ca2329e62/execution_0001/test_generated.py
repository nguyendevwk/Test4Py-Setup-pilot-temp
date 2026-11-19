import os
import sys
import pytest
from pathlib import Path
from flutils.pathutils import find_paths, normalize_path

# Helper to create a file and return its Path
def _create_file(tmp_path, name):
    file_path = tmp_path / name
    file_path.write_text("test")
    return file_path

def test_find_paths_with_glob(tmp_path):
    """Normal case: pattern matches multiple files and directories."""
    # Create files and a subdirectory
    file1 = _create_file(tmp_path, "file_one.txt")
    file2 = _create_file(tmp_path, "file_two.txt")
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    subfile = _create_file(subdir, "inner.txt")

    # Use glob pattern to match all .txt files in tmp_path
    pattern = str(tmp_path / "*.txt")
    matched = list(find_paths(pattern))

    # Assert that all expected files are found
    assert set(matched) == {file1, file2}
    # Ensure subdirectory file is not matched by the pattern
    assert subfile not in matched

def test_find_paths_no_matches(tmp_path):
    """Boundary case: pattern matches nothing."""
    # Create a file that does not match the pattern
    _create_file(tmp_path, "image.png")

    # Pattern that looks for .txt files
    pattern = str(tmp_path / "*.txt")
    matched = list(find_paths(pattern))

    # Expect an empty list
    assert matched == []

def test_find_paths_with_bytes_pattern(tmp_path):
    """Error/edge case: pattern provided as bytes."""
    # Create a file to match
    file_path = _create_file(tmp_path, "data.bin")

    # Convert pattern to bytes
    pattern_bytes = str(tmp_path / "*.bin").encode()
    matched = list(find_paths(pattern_bytes))

    # Assert that the file is found
    assert matched == [file_path]

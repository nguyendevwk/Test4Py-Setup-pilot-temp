import os
import sys
import pytest
from pathlib import Path
from flutils.pathutils import find_paths

def test_find_paths_basic(tmp_path: Path):
    """Verify that find_paths yields all matching files in a directory."""
    # Create a temporary directory structure
    (tmp_path / "file1.txt").write_text("a")
    (tmp_path / "file2.log").write_text("b")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "file3.txt").write_text("c")

    # Pattern that matches all .txt files in the root of tmp_path
    pattern = tmp_path / "*.txt"
    result = list(find_paths(pattern))

    # Expected paths: file1.txt only (file3.txt is in subdirectory)
    expected = {tmp_path / "file1.txt"}
    assert set(result) == expected, f"Expected {expected}, got {set(result)}"

def test_find_paths_tilde(tmp_path: Path, monkeypatch):
    """Verify that a tilde in the pattern is expanded to the current user's home directory."""
    # Ensure the temporary directory is inside the user's home for the test
    home = Path.home()
    test_dir = home / "flutils_test_dir"
    test_dir.mkdir(exist_ok=True)
    try:
        # Create a file in the home directory
        (test_dir / "file.txt").write_text("content")

        # Pattern using tilde
        pattern = f"~/{test_dir.name}/file.txt"
        result = list(find_paths(pattern))

        # Should find the file we just created
        expected = {test_dir / "file.txt"}
        assert set(result) == expected, f"Expected {expected}, got {set(result)}"
    finally:
        # Clean up the created file and directory
        (test_dir / "file.txt").unlink()
        test_dir.rmdir()

def test_find_paths_no_match(tmp_path: Path):
    """Verify that find_paths yields nothing when no files match the pattern."""
    # Create a file that does not match the pattern
    (tmp_path / "keep.txt").write_text("keep")

    # Pattern that matches .log files, which do not exist
    pattern = tmp_path / "*.log"
    result = list(find_paths(pattern))

    # Expect an empty list
    assert result == [], f"Expected empty list, got {result}"

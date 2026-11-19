import os
import sys
import pytest
from pathlib import Path
from flutils.pathutils import find_paths, normalize_path

@pytest.mark.parametrize("pattern_type", [str, bytes, Path])
def test_find_paths_basic(tmp_path, pattern_type):
    """Test that find_paths correctly expands a simple glob pattern."""
    # Create a temporary directory structure
    dir_one = tmp_path / "dir_one"
    dir_one.mkdir()
    file_one = tmp_path / "file_one.txt"
    file_one.write_text("content")
    # Use a pattern that matches both the file and the directory
    if pattern_type is bytes:
        pattern = (str(tmp_path) + "/*").encode()
    else:
        pattern = pattern_type(str(tmp_path) + "/*")
    # Collect results
    results = list(find_paths(pattern))
    # Normalize expected paths
    expected = {dir_one.resolve(), file_one.resolve()}
    # Assert that the generator yields the expected paths
    assert set(results) == expected
    # Ensure the returned objects are Path instances of the correct type
    for p in results:
        assert isinstance(p, Path)
        assert p.is_absolute()

def test_find_paths_no_matches(tmp_path):
    """Test that find_paths yields nothing when the pattern matches no files."""
    # Pattern that matches nothing
    pattern = tmp_path / "nonexistent_*"
    results = list(find_paths(pattern))
    # Assert that the generator is empty
    assert results == []

def test_find_paths_home_expansion(tmp_path, monkeypatch):
    """Test that find_paths expands the tilde (~) to the current user's home."""
    # Create a file in the user's home directory
    home = Path.home()
    test_file = home / ".flutils_test_file"
    test_file.write_text("test")
    try:
        # Use a pattern with ~
        pattern = "~/." + test_file.name
        results = list(find_paths(pattern))
        # Assert that the file is found
        assert test_file.resolve() in results
    finally:
        # Clean up the test file
        test_file.unlink()

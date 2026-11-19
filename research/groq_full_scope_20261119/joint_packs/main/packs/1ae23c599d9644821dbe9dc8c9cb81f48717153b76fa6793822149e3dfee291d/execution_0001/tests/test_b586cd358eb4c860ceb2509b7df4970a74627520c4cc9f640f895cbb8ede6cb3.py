import os
import sys
import pathlib
import pytest
from flutils.pathutils import find_paths, normalize_path

@pytest.fixture
def sample_dir(tmp_path):
    """Create a temporary directory structure for testing."""
    # Create files and subdirectories
    (tmp_path / "file_one").write_text("one")
    (tmp_path / "file_two").write_text("two")
    sub = tmp_path / "dir_one"
    sub.mkdir()
    (sub / "inner_file").write_text("inner")
    return tmp_path

def test_find_paths_with_wildcard(sample_dir):
    """Test that find_paths correctly expands a wildcard pattern."""
    # Use a pattern that matches both files and the subdirectory
    pattern = str(sample_dir / "*")
    paths = list(find_paths(pattern))
    # Convert to set of names for easier comparison
    names = {p.name for p in paths}
    assert names == {"file_one", "file_two", "dir_one"}
    # Ensure returned objects are Path instances
    assert all(isinstance(p, pathlib.Path) for p in paths)

def test_find_paths_no_matches(tmp_path):
    """Test that find_paths yields nothing when no files match."""
    # Pattern that matches nothing
    pattern = str(tmp_path / "nonexistent_*")
    paths = list(find_paths(pattern))
    assert paths == []

def test_find_paths_with_home_expansion(tmp_path, monkeypatch):
    """Test that find_paths expands the ~ to the current user's home directory."""
    # Create a file in the real home directory
    home = pathlib.Path.home()
    test_file = home / ".flutils_test_file"
    try:
        test_file.write_text("test")
        # Patch normalize_path to return a Path that uses the real home
        monkeypatch.setattr(
            "flutils.pathutils.normalize_path",
            lambda p: pathlib.Path(p).expanduser()
        )
        pattern = "~/.flutils_test_file"
        paths = list(find_paths(pattern))
        assert len(paths) == 1
        assert paths[0] == test_file
    finally:
        # Clean up the test file
        if test_file.exists():
            test_file.unlink()

import os
import sys
import pytest
from pathlib import Path
from flutils.pathutils import find_paths


def test_find_paths_basic(tmp_path: Path):
    """
    Verify that find_paths correctly expands a glob pattern and yields
    the expected Path objects.
    """
    # Create a directory structure
    (tmp_path / "dir_one").mkdir()
    (tmp_path / "file_one").write_text("content")
    (tmp_path / "file_two").write_text("content")

    # Use a pattern that matches all items in the temporary directory
    pattern = str(tmp_path) + "/*"
    result = list(find_paths(pattern))

    # All items should be returned as Path objects
    expected = {tmp_path / "dir_one", tmp_path / "file_one", tmp_path / "file_two"}
    assert set(result) == expected
    # Ensure the returned objects are Path instances
    assert all(isinstance(p, Path) for p in result)


def test_find_paths_bytes(tmp_path: Path):
    """
    Verify that find_paths accepts a bytes pattern and yields the same
    results as a string pattern.
    """
    # Create a file in the temporary directory
    file_path = tmp_path / "sample.txt"
    file_path.write_text("data")

    # Pattern as bytes
    pattern_bytes = (str(tmp_path) + "/*.txt").encode()
    result_bytes = list(find_paths(pattern_bytes))

    # Pattern as string
    pattern_str = str(tmp_path) + "/*.txt"
    result_str = list(find_paths(pattern_str))

    # Both results should be identical
    assert result_bytes == result_str
    assert result_bytes == [file_path]


def test_find_paths_invalid_type(tmp_path: Path):
    """
    Verify that passing an unsupported type raises a TypeError.
    """
    # An integer is not a valid pattern type
    with pytest.raises(TypeError):
        list(find_paths(123))

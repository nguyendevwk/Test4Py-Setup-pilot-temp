import os
import sys
import pytest
from pathlib import Path
from flutils.pathutils import find_paths

def test_find_paths_with_wildcard(tmp_path):
    # Arrange: create a directory structure
    sub_dir = tmp_path / "sub"
    sub_dir.mkdir()
    file1 = tmp_path / "file1.txt"
    file2 = sub_dir / "file2.txt"
    file1.touch()
    file2.touch()

    # Act: find all .txt files in the temporary directory
    pattern = str(tmp_path) + "/*.txt"
    found = list(find_paths(pattern))

    # Assert: both files are found, order is not guaranteed
    assert set(found) == {file1, file2}
    for p in found:
        assert p.is_file()
        assert p.suffix == ".txt"

def test_find_paths_no_matches(tmp_path):
    # Arrange: create a file that does not match the pattern
    (tmp_path / "keep.txt").touch()

    # Act: search for a pattern that matches nothing
    pattern = str(tmp_path) + "/nonexistent/*.py"
    found = list(find_paths(pattern))

    # Assert: no paths are yielded
    assert found == []

def test_find_paths_invalid_input():
    # Act & Assert: passing a non-string/non-PathLike should raise TypeError
    with pytest.raises(TypeError):
        list(find_paths(123))

import os
import stat
import tempfile
import pytest
from pathlib import Path
from flutils.pathutils import exists_as

def test_exists_as_regular_file_and_directory(tmp_path):
    # Create a regular file and a directory
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("content")
    dir_path = tmp_path / "test_dir"
    dir_path.mkdir()

    assert exists_as(file_path) == "file"
    assert exists_as(dir_path) == "directory"

def test_exists_as_symlinks(tmp_path):
    # Create a file and a directory, then symlink to them
    target_file = tmp_path / "target_file.txt"
    target_file.write_text("data")
    target_dir = tmp_path / "target_dir"
    target_dir.mkdir()

    file_link = tmp_path / "file_link"
    dir_link = tmp_path / "dir_link"
    file_link.symlink_to(target_file)
    dir_link.symlink_to(target_dir)

    # Symlinks should resolve to the target type
    assert exists_as(file_link) == "file"
    assert exists_as(dir_link) == "directory"

def test_exists_as_nonexistent_and_broken_symlink(tmp_path):
    # Non-existent path
    missing = tmp_path / "does_not_exist"
    assert exists_as(missing) == ""

    # Broken symlink (points to a non-existent target)
    broken_link = tmp_path / "broken_link"
    broken_link.symlink_to(tmp_path / "nonexistent_target")
    assert exists_as(broken_link) == ""

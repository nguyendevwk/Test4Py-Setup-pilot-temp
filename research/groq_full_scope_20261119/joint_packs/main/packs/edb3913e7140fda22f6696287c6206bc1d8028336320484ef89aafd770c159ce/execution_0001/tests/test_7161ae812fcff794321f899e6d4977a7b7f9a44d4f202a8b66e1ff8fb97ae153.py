import os
import stat
import tempfile
import pathlib
import pytest
from flutils.pathutils import exists_as

def test_exists_as_file_and_directory(tmp_path):
    # Create a regular file
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("content")
    assert exists_as(file_path) == "file"

    # Create a directory
    dir_path = tmp_path / "test_dir"
    dir_path.mkdir()
    assert exists_as(dir_path) == "directory"

def test_exists_as_symlink_to_file(tmp_path):
    # Create a regular file and a symlink pointing to it
    target = tmp_path / "target.txt"
    target.write_text("data")
    link = tmp_path / "link.txt"
    link.symlink_to(target)
    # The symlink should be reported as a file
    assert exists_as(link) == "file"

def test_exists_as_nonexistent_and_broken_symlink(tmp_path):
    # Non-existent path
    non_exist = tmp_path / "does_not_exist"
    assert exists_as(non_exist) == ""

    # Create a symlink to a non-existent target (broken symlink)
    broken_link = tmp_path / "broken_link"
    broken_link.symlink_to(tmp_path / "missing_target")
    # The broken symlink should also be reported as empty string
    assert exists_as(broken_link) == ""

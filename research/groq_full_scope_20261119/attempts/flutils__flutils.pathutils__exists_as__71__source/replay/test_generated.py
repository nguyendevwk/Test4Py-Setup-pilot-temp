import os
import sys
import pytest
from pathlib import Path
from flutils.pathutils import exists_as

def test_exists_as_file(tmp_path):
    # Create a regular file and verify the function reports 'file'
    file_path = tmp_path / "test.txt"
    file_path.write_text("content")
    assert exists_as(file_path) == "file"
    # Ensure that passing a string path works as well
    assert exists_as(str(file_path)) == "file"

def test_exists_as_directory(tmp_path):
    # Create a directory and verify the function reports 'directory'
    dir_path = tmp_path / "subdir"
    dir_path.mkdir()
    assert exists_as(dir_path) == "directory"
    # Passing a bytes path should also work
    assert exists_as(bytes(dir_path)) == "directory"

def test_exists_as_nonexistent(tmp_path):
    # Path that does not exist should return an empty string
    nonexistent = tmp_path / "does_not_exist"
    assert not nonexistent.exists()
    assert exists_as(nonexistent) == ""

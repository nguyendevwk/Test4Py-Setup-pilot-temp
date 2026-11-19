import os
import sys
import pytest
from flutils.pathutils import exists_as


def test_exists_as_file(tmp_path):
    """Verify that a regular file is reported correctly."""
    file_path = tmp_path / "test.txt"
    file_path.write_text("hello")
    assert exists_as(file_path) == "file"


def test_exists_as_directory(tmp_path):
    """Verify that a directory is reported correctly."""
    dir_path = tmp_path / "subdir"
    dir_path.mkdir()
    assert exists_as(dir_path) == "directory"


def test_exists_as_nonexistent_and_bytes(tmp_path):
    """Verify that a non‑existent path returns an empty string and that
    passing a bytes path works correctly."""
    # Non‑existent path
    non_path = tmp_path / "does_not_exist"
    assert exists_as(non_path) == ""

    # Bytes path pointing to an existing file
    file_path = tmp_path / "bytes.txt"
    file_path.write_text("bytes")
    bytes_path = str(file_path).encode(sys.getfilesystemencoding())
    assert exists_as(bytes_path) == "file"

import os
import pathlib
import tempfile
import shutil
import pytest

from flutils.pathutils import path_absent, normalize_path


def test_path_absent_removes_file(tmp_path):
    """path_absent should delete an existing file."""
    # Create a temporary file
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("content")
    assert file_path.exists()

    # Ensure the file is removed
    path_absent(file_path)
    assert not file_path.exists()


def test_path_absent_recursively_removes_directory(tmp_path):
    """path_absent should recursively delete a directory and its contents."""
    # Create a nested directory structure
    dir_path = tmp_path / "outer"
    inner_dir = dir_path / "inner"
    inner_dir.mkdir(parents=True)
    file1 = dir_path / "file1.txt"
    file2 = inner_dir / "file2.txt"
    file1.write_text("outer")
    file2.write_text("inner")

    # Verify existence before removal
    assert dir_path.exists()
    assert inner_dir.exists()
    assert file1.exists()
    assert file2.exists()

    # Remove the outer directory
    path_absent(dir_path)

    # All should be gone
    assert not dir_path.exists()
    assert not inner_dir.exists()
    assert not file1.exists()
    assert not file2.exists()


def test_path_absent_noop_when_path_missing(tmp_path):
    """path_absent should do nothing and not raise when the path does not exist."""
    missing_path = tmp_path / "nonexistent"
    assert not missing_path.exists()

    # Should not raise an exception
    path_absent(missing_path)

    # Path should still not exist
    assert not missing_path.exists()

import os
import pathlib
import pytest
from flutils.pathutils import path_absent

def test_path_absent_removes_file(tmp_path):
    # Create a temporary file
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("content")
    assert file_path.exists()

    # Ensure the file is removed
    path_absent(file_path)
    assert not file_path.exists()


def test_path_absent_removes_directory(tmp_path):
    # Create a nested directory structure with files
    dir_path = tmp_path / "nested"
    dir_path.mkdir()
    sub_dir = dir_path / "sub"
    sub_dir.mkdir()
    (sub_dir / "file.txt").write_text("data")
    assert dir_path.exists()
    assert sub_dir.exists()
    assert (sub_dir / "file.txt").exists()

    # Remove the entire directory tree
    path_absent(dir_path)
    assert not dir_path.exists()


def test_path_absent_removes_symlink(tmp_path):
    # Create a target file and a symlink to it
    target = tmp_path / "target.txt"
    target.write_text("target")
    link = tmp_path / "link.txt"
    link.symlink_to(target)
    assert link.is_symlink()
    assert link.exists()

    # Remove the symlink (not the target)
    path_absent(link)
    assert not link.exists()
    assert target.exists()

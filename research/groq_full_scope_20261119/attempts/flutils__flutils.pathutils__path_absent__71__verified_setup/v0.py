import os
import pathlib
import pytest
from flutils.pathutils import path_absent


def test_path_absent_removes_file(tmp_path: pathlib.Path) -> None:
    # Create a temporary file
    file_path = tmp_path / "temp_file.txt"
    file_path.write_text("content")
    assert file_path.exists()

    # Ensure the file is removed
    path_absent(file_path)
    assert not file_path.exists()


def test_path_absent_removes_directory(tmp_path: pathlib.Path) -> None:
    # Create a nested directory structure with files
    dir_path = tmp_path / "nested_dir"
    sub_dir = dir_path / "sub"
    sub_dir.mkdir(parents=True)
    (sub_dir / "file1.txt").write_text("data")
    (dir_path / "file2.txt").write_text("more data")
    assert dir_path.exists()
    assert (sub_dir / "file1.txt").exists()

    # Ensure the entire directory tree is removed
    path_absent(dir_path)
    assert not dir_path.exists()


def test_path_absent_handles_symlink_and_nonexistent(tmp_path: pathlib.Path) -> None:
    # Create a file and a symlink to it
    target_file = tmp_path / "target.txt"
    target_file.write_text("target")
    symlink_path = tmp_path / "link.txt"
    symlink_path.symlink_to(target_file)
    assert symlink_path.is_symlink()
    assert symlink_path.exists()

    # Remove the symlink
    path_absent(symlink_path)
    assert not symlink_path.exists()
    # Target file should still exist
    assert target_file.exists()

    # Call path_absent on a non-existent path; should not raise
    non_existent = tmp_path / "does_not_exist.txt"
    assert not non_existent.exists()
    path_absent(non_existent)  # should complete silently
    assert not non_existent.exists()

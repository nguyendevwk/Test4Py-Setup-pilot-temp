import os
import pathlib
import pytest
from flutils.pathutils import path_absent, normalize_path


def test_path_absent_removes_file(tmp_path: pathlib.Path) -> None:
    """path_absent should delete an existing file."""
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("content")
    assert file_path.exists()
    path_absent(file_path)
    assert not file_path.exists()


def test_path_absent_removes_directory_recursively(tmp_path: pathlib.Path) -> None:
    """path_absent should recursively delete a directory and its contents."""
    dir_path = tmp_path / "test_dir"
    dir_path.mkdir()
    (dir_path / "subdir").mkdir()
    (dir_path / "subdir" / "file.txt").write_text("data")
    assert dir_path.exists()
    assert (dir_path / "subdir" / "file.txt").exists()
    path_absent(dir_path)
    assert not dir_path.exists()


def test_path_absent_handles_symlink_and_relative_path(tmp_path: pathlib.Path) -> None:
    """path_absent should remove symlinks and work with relative paths."""
    target_file = tmp_path / "target.txt"
    target_file.write_text("target")
    symlink_path = tmp_path / "link.txt"
    symlink_path.symlink_to(target_file)
    assert symlink_path.is_symlink()
    # Use a relative path string
    relative_path = os.path.relpath(symlink_path, start=os.getcwd())
    path_absent(relative_path)
    assert not symlink_path.exists()
    # Ensure the target file still exists
    assert target_file.exists()

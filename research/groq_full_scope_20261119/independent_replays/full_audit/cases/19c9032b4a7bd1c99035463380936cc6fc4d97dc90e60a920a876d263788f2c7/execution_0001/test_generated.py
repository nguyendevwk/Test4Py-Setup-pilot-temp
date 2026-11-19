import os
import pathlib
import pytest
from flutils.pathutils import path_absent


def test_path_absent_removes_file(tmp_path: pathlib.Path) -> None:
    """path_absent should delete a regular file."""
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("content")
    assert file_path.exists()
    path_absent(file_path)
    assert not file_path.exists()


def test_path_absent_removes_directory(tmp_path: pathlib.Path) -> None:
    """path_absent should recursively delete a directory and its contents."""
    dir_path = tmp_path / "test_dir"
    dir_path.mkdir()
    (dir_path / "subfile.txt").write_text("sub")
    (dir_path / "subdir").mkdir()
    (dir_path / "subdir" / "inner.txt").write_text("inner")
    assert dir_path.exists()
    path_absent(dir_path)
    assert not dir_path.exists()


def test_path_absent_handles_symlink(tmp_path: pathlib.Path) -> None:
    """path_absent should unlink a symbolic link without affecting the target."""
    target = tmp_path / "target.txt"
    target.write_text("target")
    link = tmp_path / "link.txt"
    link.symlink_to(target)
    assert link.is_symlink()
    assert target.exists()
    path_absent(link)
    assert not link.exists()
    assert target.exists()

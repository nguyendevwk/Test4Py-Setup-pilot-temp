import os
import stat
import tempfile
import pytest
from pathlib import Path
from flutils.pathutils import exists_as


def test_exists_as_regular_file(tmp_path: Path):
    # Create a regular file
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("content")
    assert exists_as(file_path) == "file"

    # Ensure that a non-existent file returns empty string
    missing_path = tmp_path / "missing.txt"
    assert exists_as(missing_path) == ""


def test_exists_as_directory_and_symlink(tmp_path: Path):
    # Create a directory
    dir_path = tmp_path / "test_dir"
    dir_path.mkdir()
    assert exists_as(dir_path) == "directory"

    # Create a symlink to the directory
    symlink_path = tmp_path / "link_to_dir"
    symlink_path.symlink_to(dir_path, target_is_directory=True)
    assert exists_as(symlink_path) == "directory"

    # Create a broken symlink
    broken_symlink = tmp_path / "broken_link"
    broken_symlink.symlink_to(tmp_path / "nonexistent")
    assert exists_as(broken_symlink) == ""


def test_exists_as_special_file(tmp_path: Path):
    # Create a FIFO (named pipe)
    fifo_path = tmp_path / "test_fifo"
    os.mkfifo(fifo_path)
    assert exists_as(fifo_path) == "FIFO"

    # Create a character device (requires root; skip if not possible)
    if hasattr(os, "mknod"):
        char_path = tmp_path / "test_char"
        os.mknod(char_path, mode=stat.S_IFCHR | 0o666, device=os.makedev(1, 3))
        assert exists_as(char_path) == "char device"

    # Create a block device (requires root; skip if not possible)
    if hasattr(os, "mknod"):
        block_path = tmp_path / "test_block"
        os.mknod(block_path, mode=stat.S_IFBLK | 0o666, device=os.makedev(8, 0))
        assert exists_as(block_path) == "block device"

import os
import stat
import pytest
from flutils.pathutils import chmod, normalize_path

def test_chmod_file_and_directory(tmp_path):
    # Create a file and a directory
    file_path = tmp_path / "file.txt"
    dir_path = tmp_path / "subdir"
    file_path.write_text("content")
    dir_path.mkdir()

    # Ensure initial permissions are not the target ones
    file_path.chmod(0o644)
    dir_path.chmod(0o755)

    # Apply chmod with custom modes
    chmod(file_path, mode_file=0o600, mode_dir=0o700)
    chmod(dir_path, mode_file=0o600, mode_dir=0o700)

    # Verify permissions
    assert stat.S_IMODE(file_path.stat().st_mode) == 0o600
    assert stat.S_IMODE(dir_path.stat().st_mode) == 0o700

def test_chmod_glob_pattern(tmp_path):
    # Create multiple files and directories
    (tmp_path / "a.txt").write_text("a")
    (tmp_path / "b.txt").write_text("b")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "c.txt").write_text("c")

    # Set initial permissions
    for p in tmp_path.glob("*"):
        p.chmod(0o644)
    for p in tmp_path.glob("sub/*"):
        p.chmod(0o644)

    # Apply chmod to all items in tmp_path
    chmod(tmp_path / "*", mode_file=0o600, mode_dir=0o700, include_parent=True)

    # Parent directory should have mode_dir
    assert stat.S_IMODE(tmp_path.stat().st_mode) == 0o700

    # Files should have mode_file
    for p in tmp_path.glob("*"):
        if p.is_file():
            assert stat.S_IMODE(p.stat().st_mode) == 0o600
        elif p.is_dir():
            assert stat.S_IMODE(p.stat().st_mode) == 0o700

def test_chmod_nonexistent_path(tmp_path):
    # Path that does not exist
    nonexistent = tmp_path / "does_not_exist.txt"

    # Ensure it does not exist
    assert not nonexistent.exists()

    # Capture the current permissions of the parent directory
    parent_mode_before = stat.S_IMODE(tmp_path.stat().st_mode)

    # Call chmod; should not raise and should leave everything unchanged
    chmod(nonexistent, mode_file=0o600, mode_dir=0o700)

    # Verify parent directory permissions unchanged
    assert stat.S_IMODE(tmp_path.stat().st_mode) == parent_mode_before
    # Verify nonexistent path still does not exist
    assert not nonexistent.exists()

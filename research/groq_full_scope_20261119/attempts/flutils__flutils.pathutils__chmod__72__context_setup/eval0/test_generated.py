import os
import stat
import tempfile
import pytest
from flutils.pathutils import chmod, normalize_path

def test_chmod_single_file(tmp_path):
    """Changing mode of a single file works."""
    file_path = tmp_path / "testfile.txt"
    file_path.write_text("content")
    # Ensure initial mode is not the target mode
    file_path.chmod(0o644)
    chmod(file_path, mode_file=0o600, mode_dir=0o700)
    assert stat.S_IMODE(file_path.stat().st_mode) == 0o600

def test_chmod_glob_and_parent(tmp_path):
    """Glob pattern changes all matching files and optionally parent."""
    # Create a directory tree
    dir_path = tmp_path / "dir"
    dir_path.mkdir()
    (dir_path / "a.txt").write_text("a")
    (dir_path / "b.txt").write_text("b")
    # Set initial modes
    dir_path.chmod(0o777)
    for f in dir_path.iterdir():
        f.chmod(0o666)
    # Apply chmod with glob and include_parent=True
    chmod(f"{tmp_path}/dir/*", mode_file=0o644, mode_dir=0o700, include_parent=True)
    # Parent directory should be unchanged
    assert stat.S_IMODE(tmp_path.stat().st_mode) == 0o755
    # Directory should be unchanged
    assert stat.S_IMODE(dir_path.stat().st_mode) == 0o777
    # Files should have new mode
    for f in dir_path.iterdir():
        assert stat.S_IMODE(f.stat().st_mode) == 0o644

def test_chmod_nonexistent_path(tmp_path):
    """No exception is raised and nothing changes for a nonexistent path."""
    nonexistent = tmp_path / "does_not_exist.txt"
    # Ensure path does not exist
    assert not nonexistent.exists()
    # Capture current mode of tmp_path to compare later
    original_mode = stat.S_IMODE(tmp_path.stat().st_mode)
    # Call chmod; should silently do nothing
    chmod(nonexistent, mode_file=0o600, mode_dir=0o700)
    # Verify that tmp_path mode is unchanged
    assert stat.S_IMODE(tmp_path.stat().st_mode) == original_mode

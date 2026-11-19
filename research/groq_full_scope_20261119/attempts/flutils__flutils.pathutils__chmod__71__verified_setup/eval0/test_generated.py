import os
import stat
import pytest
from flutils.pathutils import chmod, normalize_path

def test_chmod_file_and_directory(tmp_path):
    # Create a file and a directory
    file_path = tmp_path / "testfile.txt"
    dir_path = tmp_path / "testdir"
    file_path.write_text("content")
    dir_path.mkdir()

    # Apply chmod with custom modes
    chmod(file_path, mode_file=0o644, mode_dir=0o755)
    chmod(dir_path, mode_file=0o644, mode_dir=0o755)

    # Verify file mode
    file_mode = stat.S_IMODE(os.lstat(file_path).st_mode)
    assert file_mode == 0o644, f"Expected 0o644, got {oct(file_mode)}"

    # Verify directory mode
    dir_mode = stat.S_IMODE(os.lstat(dir_path).st_mode)
    assert dir_mode == 0o755, f"Expected 0o755, got {oct(dir_mode)}"

def test_chmod_glob_and_include_parent(tmp_path):
    # Setup nested structure
    (tmp_path / "a").mkdir()
    (tmp_path / "a" / "b").mkdir()
    (tmp_path / "a" / "b" / "file.txt").write_text("data")
    (tmp_path / "a" / "c.txt").write_text("data")

    # Glob pattern to change all files and dirs under tmp_path
    pattern = normalize_path(tmp_path / "**")
    chmod(pattern, mode_file=0o600, mode_dir=0o700, include_parent=True)

    # Check modes
    for p in [tmp_path, tmp_path / "a", tmp_path / "a" / "b"]:
        mode = stat.S_IMODE(os.lstat(p).st_mode)
        assert mode == 0o700, f"{p} mode should be 0o700, got {oct(mode)}"

    for p in [tmp_path / "a" / "c.txt", tmp_path / "a" / "b" / "file.txt"]:
        mode = stat.S_IMODE(os.lstat(p).st_mode)
        assert mode == 0o600, f"{p} mode should be 0o600, got {oct(mode)}"

def test_chmod_nonexistent_path(tmp_path):
    # Path that does not exist
    nonexistent = tmp_path / "does_not_exist.txt"

    # Ensure no exception is raised and nothing is created
    chmod(nonexistent, mode_file=0o644, mode_dir=0o755)

    # Path should still not exist
    assert not nonexistent.exists(), "Nonexistent path should remain nonexistent"

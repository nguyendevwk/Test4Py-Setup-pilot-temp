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

    # Apply chmod with custom modes
    chmod(file_path, mode_file=0o644, mode_dir=0o755)
    chmod(dir_path, mode_file=0o644, mode_dir=0o755)

    # Verify file mode
    file_mode = stat.S_IMODE(os.lstat(file_path).st_mode)
    assert file_mode == 0o644, f"Expected 0o644, got {oct(file_mode)}"

    # Verify directory mode
    dir_mode = stat.S_IMODE(os.lstat(dir_path).st_mode)
    assert dir_mode == 0o755, f"Expected 0o755, got {oct(dir_mode)}"

def test_chmod_glob_pattern_and_include_parent(tmp_path):
    # Setup nested structure
    (tmp_path / "a").mkdir()
    (tmp_path / "a" / "b.txt").write_text("data")
    (tmp_path / "a" / "c").mkdir()
    (tmp_path / "a" / "c" / "d.txt").write_text("more")

    # Apply glob pattern to change all files to 0o600 and dirs to 0o700
    chmod(tmp_path / "a/**", mode_file=0o600, mode_dir=0o700, include_parent=True)

    # Check parent directory of pattern (tmp_path/a) mode
    parent_mode = stat.S_IMODE(os.lstat(tmp_path / "a").st_mode)
    assert parent_mode == 0o700, f"Parent dir mode should be 0o700, got {oct(parent_mode)}"

    # Check nested file and dir modes
    for path in [tmp_path / "a" / "b.txt", tmp_path / "a" / "c" / "d.txt"]:
        mode = stat.S_IMODE(os.lstat(path).st_mode)
        assert mode == 0o600, f"File {path} mode should be 0o600, got {oct(mode)}"

    for path in [tmp_path / "a" / "c"]:
        mode = stat.S_IMODE(os.lstat(path).st_mode)
        assert mode == 0o700, f"Dir {path} mode should be 0o700, got {oct(mode)}"

def test_chmod_nonexistent_path(tmp_path):
    # Path that does not exist
    nonexistent = tmp_path / "does_not_exist.txt"

    # Capture current permissions of a known file for comparison
    known_file = tmp_path / "known.txt"
    known_file.write_text("hello")
    original_mode = stat.S_IMODE(os.lstat(known_file).st_mode)

    # Call chmod on nonexistent path; should not raise and not modify known file
    chmod(nonexistent, mode_file=0o644, mode_dir=0o755)

    # Verify known file remains unchanged
    new_mode = stat.S_IMODE(os.lstat(known_file).st_mode)
    assert new_mode == original_mode, f"Mode changed unexpectedly to {oct(new_mode)}"

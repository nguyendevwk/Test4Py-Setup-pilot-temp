import os
import stat
import pytest
from flutils.pathutils import chmod, normalize_path

def test_chmod_file_and_directory(tmp_path):
    # Create a file and a directory
    file_path = tmp_path / "test_file.txt"
    dir_path = tmp_path / "test_dir"
    file_path.write_text("content")
    dir_path.mkdir()

    # Apply chmod with custom modes
    chmod(file_path, mode_file=0o644, mode_dir=0o700)
    chmod(dir_path, mode_file=0o644, mode_dir=0o700)

    # Verify file mode
    file_mode = stat.S_IMODE(os.lstat(file_path).st_mode)
    assert file_mode == 0o644, f"Expected file mode 0o644, got {oct(file_mode)}"

    # Verify directory mode
    dir_mode = stat.S_IMODE(os.lstat(dir_path).st_mode)
    assert dir_mode == 0o700, f"Expected dir mode 0o700, got {oct(dir_mode)}"

def test_chmod_glob_and_include_parent(tmp_path):
    # Setup nested structure
    (tmp_path / "sub1").mkdir()
    (tmp_path / "sub1" / "file1.txt").write_text("a")
    (tmp_path / "sub2").mkdir()
    (tmp_path / "sub2" / "file2.txt").write_text("b")

    # Glob pattern to change all files and dirs inside tmp_path
    glob_pattern = normalize_path(tmp_path / "**")
    chmod(glob_pattern, mode_file=0o600, mode_dir=0o700, include_parent=True)

    # Check each file and directory mode
    for path in [tmp_path / "sub1", tmp_path / "sub1" / "file1.txt",
                 tmp_path / "sub2", tmp_path / "sub2" / "file2.txt"]:
        mode = stat.S_IMODE(os.lstat(path).st_mode)
        expected = 0o700 if path.is_dir() else 0o600
        assert mode == expected, f"{path} mode {oct(mode)} != {oct(expected)}"

    # Parent directory should also be changed due to include_parent
    parent_mode = stat.S_IMODE(os.lstat(tmp_path).st_mode)
    assert parent_mode == 0o700, f"Parent mode {oct(parent_mode)} != 0o700"

def test_chmod_nonexistent_path(tmp_path):
    # Path that does not exist
    nonexistent = tmp_path / "does_not_exist.txt"

    # Capture current mode of parent directory
    parent_mode_before = stat.S_IMODE(os.lstat(tmp_path).st_mode)

    # Call chmod on nonexistent path
    chmod(nonexistent, mode_file=0o644, mode_dir=0o700)

    # Ensure no exception and parent mode unchanged
    parent_mode_after = stat.S_IMODE(os.lstat(tmp_path).st_mode)
    assert parent_mode_before == parent_mode_after, "Parent mode changed unexpectedly"

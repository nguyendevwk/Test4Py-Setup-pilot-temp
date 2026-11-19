import os
import stat
import pytest
from flutils.pathutils import chmod, normalize_path

def test_chmod_file(tmp_path):
    # Create a file and set an initial mode
    file_path = tmp_path / "testfile.txt"
    file_path.write_text("content")
    file_path.chmod(0o644)
    # Apply chmod with a different mode
    chmod(file_path, mode_file=0o600, mode_dir=0o700)
    # Verify the file mode changed to 0o600
    mode = stat.S_IMODE(os.stat(file_path).st_mode)
    assert mode == 0o600, f"Expected 0o600, got {oct(mode)}"

def test_chmod_directory(tmp_path):
    # Create a directory and set an initial mode
    dir_path = tmp_path / "testdir"
    dir_path.mkdir()
    dir_path.chmod(0o755)
    # Apply chmod with a different mode
    chmod(dir_path, mode_file=0o600, mode_dir=0o700)
    # Verify the directory mode changed to 0o700
    mode = stat.S_IMODE(os.stat(dir_path).st_mode)
    assert mode == 0o700, f"Expected 0o700, got {oct(mode)}"

def test_chmod_glob_include_parent(tmp_path):
    # Create a directory structure with files
    parent = tmp_path / "parent"
    parent.mkdir()
    sub_dir = parent / "subdir"
    sub_dir.mkdir()
    file1 = parent / "file1.txt"
    file1.write_text("a")
    file2 = sub_dir / "file2.txt"
    file2.write_text("b")
    # Set initial modes
    parent.chmod(0o755)
    sub_dir.chmod(0o755)
    file1.chmod(0o644)
    file2.chmod(0o644)
    # Apply chmod to all items under parent, include parent
    glob_path = normalize_path(str(parent) + "/**")
    chmod(glob_path, mode_file=0o600, mode_dir=0o700, include_parent=True)
    # Verify parent directory mode changed
    assert stat.S_IMODE(os.stat(parent).st_mode) == 0o700
    # Verify subdirectory mode changed
    assert stat.S_IMODE(os.stat(sub_dir).st_mode) == 0o700
    # Verify files mode changed
    assert stat.S_IMODE(os.stat(file1).st_mode) == 0o600
    assert stat.S_IMODE(os.stat(file2).st_mode) == 0o600

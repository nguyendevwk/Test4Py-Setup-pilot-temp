import os
import stat
import tempfile
import pytest
from pathlib import Path
from flutils.pathutils import directory_present

def test_directory_present_creates_nested(tmp_path):
    # Create a nested absolute path that does not exist yet
    nested = tmp_path / "a" / "b" / "c"
    # Ensure the path is absolute
    abs_path = nested.resolve()
    # Call the function
    result = directory_present(abs_path, mode=0o755)
    # Verify the returned Path is the same absolute path
    assert result == abs_path
    # Verify all directories were created
    assert abs_path.is_dir()
    assert (abs_path.parent / "b").is_dir()
    assert (abs_path.parent.parent / "a").is_dir()
    # Verify permissions were applied
    assert stat.S_IMODE(abs_path.stat().st_mode) == 0o755

def test_directory_present_raises_on_glob(tmp_path):
    # Use a glob pattern in the path
    glob_path = tmp_path / "foo*"
    with pytest.raises(ValueError) as excinfo:
        directory_present(glob_path)
    assert "glob patterns" in str(excinfo.value)

def test_directory_present_raises_on_existing_file(tmp_path):
    # Create a file at the target location
    file_path = tmp_path / "existing_file"
    file_path.write_text("content")
    # Attempt to create a directory at the same path
    with pytest.raises(FileExistsError) as excinfo:
        directory_present(file_path)
    assert "already exists as a file" in str(excinfo.value)

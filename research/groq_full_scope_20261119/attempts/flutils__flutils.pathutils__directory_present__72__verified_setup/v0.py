import os
import pytest
from pathlib import Path
from flutils.pathutils import directory_present

def test_directory_present_creates_nested(tmp_path):
    # Create a nested directory path that does not exist yet
    nested = tmp_path / "a" / "b" / "c"
    # Ensure the path is absolute
    abs_path = nested.resolve()
    # Call the function
    result = directory_present(abs_path)
    # The function should return a Path object equal to the resolved path
    assert isinstance(result, Path)
    assert result == abs_path
    # The directory should now exist
    assert abs_path.is_dir()
    # All intermediate directories should also exist
    assert (abs_path.parent).is_dir()
    assert (abs_path.parent.parent).is_dir()

def test_directory_present_raises_on_existing_file(tmp_path):
    # Create a file where the directory should be
    file_path = tmp_path / "existing_file"
    file_path.write_text("content")
    # Resolve to absolute path
    abs_path = file_path.resolve()
    # Attempting to create a directory at this path should raise FileExistsError
    with pytest.raises(FileExistsError) as excinfo:
        directory_present(abs_path)
    # The error message should mention the existing file
    assert "existing as a file" in str(excinfo.value)

def test_directory_present_raises_on_file_parent(tmp_path):
    # Create a file that will be a parent of the target directory
    parent_file = tmp_path / "parent_file"
    parent_file.write_text("content")
    # Target directory path inside the file's parent
    target_dir = parent_file / "child_dir"
    abs_target = target_dir.resolve()
    # Attempting to create the directory should raise FileExistsError
    with pytest.raises(FileExistsError) as excinfo:
        directory_present(abs_target)
    # The error message should mention the parent file
    assert "parent path" in str(excinfo.value)

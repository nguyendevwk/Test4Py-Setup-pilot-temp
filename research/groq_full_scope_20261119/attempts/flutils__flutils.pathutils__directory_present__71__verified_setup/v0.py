import os
import stat
import tempfile
import pytest
from pathlib import Path
from flutils.pathutils import directory_present

def test_directory_present_creates_missing_dirs(tmp_path):
    # Create a nested path that does not exist yet
    nested = tmp_path / "a" / "b" / "c"
    # Ensure the path is absolute
    abs_path = nested.resolve()
    # Call the function
    result = directory_present(abs_path, mode=0o755)
    # The result should be a Path object pointing to the created directory
    assert isinstance(result, Path)
    assert result == abs_path
    # All directories should now exist
    assert abs_path.is_dir()
    assert (abs_path.parent / "b").is_dir()
    assert (abs_path.parent.parent / "a").is_dir()
    # Mode should be applied to the deepest directory
    assert stat.S_IMODE(abs_path.stat().st_mode) == 0o755

def test_directory_present_raises_on_existing_file(tmp_path):
    # Create a file at the target location
    file_path = tmp_path / "existing_file"
    file_path.write_text("content")
    # Ensure the path is absolute
    abs_path = file_path.resolve()
    # Attempting to create a directory at this path should raise FileExistsError
    with pytest.raises(FileExistsError) as excinfo:
        directory_present(abs_path)
    assert "already exists as a file" in str(excinfo.value)

def test_directory_present_rejects_glob_pattern(tmp_path):
    # Use a glob pattern in the path
    glob_path = tmp_path / "some*pattern"
    abs_path = glob_path.resolve()
    # The function should raise ValueError for glob patterns
    with pytest.raises(ValueError) as excinfo:
        directory_present(abs_path)
    assert "must NOT contain any glob patterns" in str(excinfo.value)

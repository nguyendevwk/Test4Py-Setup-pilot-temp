import os
import stat
import pytest
from pathlib import Path
from flutils.pathutils import directory_present, exists_as


def test_directory_present_creates_missing_dirs(tmp_path):
    # Create a nested path that does not exist yet
    nested = tmp_path / "a" / "b" / "c"
    # Ensure the path is not present
    assert not nested.exists()

    # Call the function
    result = directory_present(nested, mode=0o755)

    # The returned Path should be absolute
    assert result.is_absolute()
    # The directory should now exist
    assert nested.is_dir()
    # Mode should be applied
    assert stat.S_IMODE(nested.stat().st_mode) == 0o755
    # The function returns a Path object (not the same instance as input)
    assert isinstance(result, Path)
    assert result != nested


def test_directory_present_raises_on_glob_pattern(tmp_path):
    # Use a glob pattern in the path
    glob_path = tmp_path / "foo*"
    with pytest.raises(ValueError) as excinfo:
        directory_present(glob_path)
    assert "glob patterns" in str(excinfo.value)


def test_directory_present_raises_when_path_is_file(tmp_path):
    # Create a file where the directory should be
    file_path = tmp_path / "existing_file"
    file_path.write_text("content")
    assert file_path.is_file()

    # Attempt to create a directory at the same location
    with pytest.raises(FileExistsError) as excinfo:
        directory_present(file_path)
    assert "already exists as a file" in str(excinfo.value)

    # Verify that the file was not altered
    assert file_path.is_file()
    assert file_path.read_text() == "content"

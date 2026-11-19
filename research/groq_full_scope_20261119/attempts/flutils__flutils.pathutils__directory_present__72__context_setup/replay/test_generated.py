import os
import stat
import tempfile
import pytest
from pathlib import Path

from flutils.pathutils import directory_present, exists_as


def test_directory_present_creates_missing_dirs(tmp_path):
    # Create a nested path that does not exist yet
    nested = tmp_path / "a" / "b" / "c"
    # Ensure the parent directories are removed
    assert not nested.exists()
    # Call directory_present to create the whole tree
    result = directory_present(nested, mode=0o755)
    # The returned Path should be absolute and equal to the nested path
    assert result.is_absolute()
    assert result == nested
    # All directories should now exist
    assert nested.is_dir()
    assert (nested.parent).is_dir()
    assert (nested.parent.parent).is_dir()
    # Mode should be applied to the deepest directory
    assert stat.S_IMODE(nested.stat().st_mode) == 0o755


def test_directory_present_raises_on_glob_pattern(tmp_path):
    # Use a glob pattern in the path
    glob_path = tmp_path / "foo*"
    # directory_present should raise ValueError because of '*'
    with pytest.raises(ValueError) as excinfo:
        directory_present(glob_path)
    assert "glob patterns" in str(excinfo.value)


def test_directory_present_raises_on_existing_file(tmp_path):
    # Create a file at the target path
    file_path = tmp_path / "existing_file.txt"
    file_path.write_text("content")
    # directory_present should raise FileExistsError because path is a file
    with pytest.raises(FileExistsError) as excinfo:
        directory_present(file_path)
    assert "already exists as a file" in str(excinfo.value)

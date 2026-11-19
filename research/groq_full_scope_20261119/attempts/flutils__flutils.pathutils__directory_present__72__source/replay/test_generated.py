import os
import getpass
import grp
import pytest
from pathlib import Path
from flutils.pathutils import directory_present

@pytest.fixture
def user_and_group():
    """Return current user and group names for chown."""
    return getpass.getuser(), grp.getgrgid(os.getgid()).gr_name

def test_directory_present_creates_missing_dirs(tmp_path, user_and_group):
    """directory_present should create missing directories and set mode."""
    # Build a nested path that does not exist
    nested = tmp_path / "level1" / "level2" / "level3"
    # Ensure it does not exist yet
    assert not nested.exists()

    # Call directory_present with explicit mode and ownership
    result = directory_present(
        nested,
        mode=0o755,
        user=user_and_group[0],
        group=user_and_group[1],
    )

    # The returned Path should be absolute and equal to the nested path
    assert isinstance(result, Path)
    assert result.is_absolute()
    assert result == nested

    # The directory should now exist
    assert nested.is_dir()

    # Mode should be applied (owner read/write/execute, group and others read/execute)
    assert oct(nested.stat().st_mode & 0o777) == "0o755"

def test_directory_present_raises_on_glob(tmp_path):
    """directory_present should raise ValueError if path contains a glob pattern."""
    glob_path = tmp_path / "foo*"
    with pytest.raises(ValueError, match="must NOT contain any glob patterns"):
        directory_present(glob_path)

def test_directory_present_raises_on_existing_file(tmp_path, user_and_group):
    """directory_present should raise FileExistsError if path exists as a file."""
    # Create a file at the target location
    file_path = tmp_path / "existing_file"
    file_path.write_text("content")
    assert file_path.is_file()

    with pytest.raises(FileExistsError, match="already exists as a file"):
        directory_present(
            file_path,
            user=user_and_group[0],
            group=user_and_group[1],
        )

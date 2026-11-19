import os
import pwd
import grp
import pytest
from flutils.pathutils import chown, get_os_user, get_os_group, normalize_path

def test_chown_nonexistent_path(tmp_path):
    """Calling chown on a path that does not exist should silently succeed."""
    nonexistent = tmp_path / "does_not_exist.txt"
    # Ensure the path truly does not exist
    assert not nonexistent.exists()
    # Should not raise any exception
    chown(nonexistent)

def test_chown_invalid_user_raises(tmp_path):
    """Providing a non‑existent user name should raise OSError."""
    # Create a temporary file so that chown will attempt to resolve the user
    file_path = tmp_path / "file.txt"
    file_path.write_text("test")
    # Use a user name that almost certainly does not exist
    with pytest.raises(OSError) as excinfo:
        chown(file_path, user="this_user_does_not_exist")
    assert "not a valid \"login name\"" in str(excinfo.value)

def test_chown_invalid_group_raises(tmp_path):
    """Providing a non‑existent group name should raise OSError."""
    # Create a temporary file so that chown will attempt to resolve the group
    file_path = tmp_path / "file.txt"
    file_path.write_text("test")
    # Use a group name that almost certainly does not exist
    with pytest.raises(OSError) as excinfo:
        chown(file_path, group="this_group_does_not_exist")
    assert "not a valid \"group name\"" in str(excinfo.value)

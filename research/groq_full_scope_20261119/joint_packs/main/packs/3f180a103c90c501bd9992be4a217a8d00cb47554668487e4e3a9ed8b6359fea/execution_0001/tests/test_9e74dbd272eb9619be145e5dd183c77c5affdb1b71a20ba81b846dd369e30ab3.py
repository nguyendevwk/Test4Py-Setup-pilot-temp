import os
import pwd
import pytest
from flutils.pathutils import chown, get_os_user, get_os_group, normalize_path


def test_chown_noop_on_nonexistent_path(tmp_path):
    """When the path does not exist, chown should silently return."""
    non_existent = tmp_path / "does_not_exist.txt"
    # Ensure the file truly does not exist
    assert not non_existent.exists()
    # Using '-1' for both user and group leaves ownership unchanged
    chown(non_existent, user='-1', group='-1')
    # No exception should be raised and the file still does not exist
    assert not non_existent.exists()


def test_chown_invalid_user_raises(tmp_path):
    """chown should raise OSError if the user does not exist."""
    file_path = tmp_path / "file.txt"
    file_path.write_text("content")
    # Use a username that is unlikely to exist
    invalid_user = "this_user_does_not_exist_12345"
    with pytest.raises(OSError) as excinfo:
        chown(file_path, user=invalid_user, group='-1')
    # The exception message should mention the invalid user
    assert invalid_user in str(excinfo.value)


def test_chown_with_glob_and_include_parent(tmp_path):
    """chown should apply to all matched files and optionally the parent dir."""
    # Create a directory structure with two files
    subdir = tmp_path / "sub"
    subdir.mkdir()
    file1 = subdir / "a.txt"
    file2 = subdir / "b.txt"
    file1.write_text("a")
    file2.write_text("b")

    # Capture the original owner of the parent directory
    original_uid = os.stat(tmp_path).st_uid
    original_gid = os.stat(tmp_path).st_gid

    # Use '-1' to leave ownership unchanged; this will still call os.chown
    # but with -1, which is a no-op and should not raise an error.
    chown(f"{tmp_path}/sub/*", user='-1', group='-1', include_parent=True)

    # After the call, the parent directory's ownership should remain unchanged
    new_uid = os.stat(tmp_path).st_uid
    new_gid = os.stat(tmp_path).st_gid
    assert new_uid == original_uid
    assert new_gid == original_gid

    # The files should still exist and be unchanged
    assert file1.exists()
    assert file2.exists()

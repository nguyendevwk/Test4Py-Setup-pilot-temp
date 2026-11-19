import getpass
import os
import pwd
import pytest

from flutils.pathutils import get_os_user


def test_get_os_user_current_user():
    """The function should return the struct_passwd for the current user."""
    current_user = getpass.getuser()
    user_struct = get_os_user()
    assert isinstance(user_struct, pwd.struct_passwd)
    assert user_struct.pw_name == current_user
    # The uid and gid should be integers and match the OS values
    assert isinstance(user_struct.pw_uid, int)
    assert isinstance(user_struct.pw_gid, int)
    # The home directory should exist
    assert os.path.isdir(user_struct.pw_dir)


def test_get_os_user_invalid_uid_raises():
    """Providing an integer uid that does not exist should raise OSError."""
    # Use a negative uid which is guaranteed not to exist on POSIX systems
    invalid_uid = -1
    with pytest.raises(OSError) as excinfo:
        get_os_user(invalid_uid)
    assert f"The given uid: {invalid_uid}" in str(excinfo.value)


def test_get_os_user_invalid_name_raises():
    """Providing a non‑existent login name should raise OSError."""
    # Choose a name that is highly unlikely to exist
    invalid_name = "this_user_does_not_exist_123456"
    with pytest.raises(OSError) as excinfo:
        get_os_user(invalid_name)
    assert f"The given name: {invalid_name}" in str(excinfo.value)

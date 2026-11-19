import os
import pwd
import getpass
import pytest
from flutils.pathutils import get_os_user


def test_get_os_user_current_user_returns_struct_passwd():
    """When called without arguments, should return the current user struct."""
    current_user = getpass.getuser()
    user_struct = get_os_user()
    assert isinstance(user_struct, pwd.struct_passwd)
    assert user_struct.pw_name == current_user
    # The struct should contain a valid uid and gid
    assert isinstance(user_struct.pw_uid, int)
    assert isinstance(user_struct.pw_gid, int)
    # The home directory should exist
    assert os.path.isdir(user_struct.pw_dir)


def test_get_os_user_with_valid_uid_returns_struct_passwd():
    """Providing a valid uid should return the corresponding user struct."""
    # Use the current user's uid as a valid example
    uid = os.getuid()
    user_struct = get_os_user(uid)
    assert isinstance(user_struct, pwd.struct_passwd)
    assert user_struct.pw_uid == uid
    # The name should match the current user
    assert user_struct.pw_name == getpass.getuser()


def test_get_os_user_invalid_name_and_uid_raise_oserror():
    """Providing an invalid name or uid should raise OSError."""
    # Invalid name: unlikely string
    with pytest.raises(OSError) as exc_name:
        get_os_user("this_user_does_not_exist_123456")
    assert "not a valid \"login name\"" in str(exc_name.value)

    # Invalid uid: negative number
    with pytest.raises(OSError) as exc_uid:
        get_os_user(-1)
    assert "not a valid uid" in str(exc_uid.value)

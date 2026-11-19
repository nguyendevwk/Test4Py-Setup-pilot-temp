import os
import pwd
import getpass
import pytest
from flutils.pathutils import get_os_user


def test_get_os_user_current_user():
    """get_os_user() without arguments should return the current user."""
    current_user = getpass.getuser()
    user_obj = get_os_user()
    assert isinstance(user_obj, pwd.struct_passwd)
    assert user_obj.pw_name == current_user
    # The returned object should match the one from pwd.getpwnam
    expected = pwd.getpwnam(current_user)
    assert user_obj == expected


def test_get_os_user_by_uid_and_name():
    """get_os_user() should correctly resolve by uid and by name."""
    # Resolve by uid
    uid = os.getuid()
    user_by_uid = get_os_user(uid)
    assert isinstance(user_by_uid, pwd.struct_passwd)
    assert user_by_uid.pw_uid == uid

    # Resolve by name
    name = user_by_uid.pw_name
    user_by_name = get_os_user(name)
    assert isinstance(user_by_name, pwd.struct_passwd)
    assert user_by_name.pw_name == name
    # Both lookups should return the same struct
    assert user_by_uid == user_by_name


def test_get_os_user_invalid_inputs():
    """get_os_user() should raise OSError for non‑existent names or uids."""
    # Non‑existent username
    with pytest.raises(OSError) as excinfo_name:
        get_os_user("this_user_does_not_exist_12345")
    assert "not a valid \"login name\"" in str(excinfo_name.value)

    # Non‑existent uid (choose a large number unlikely to exist)
    invalid_uid = 999999
    with pytest.raises(OSError) as excinfo_uid:
        get_os_user(invalid_uid)
    assert "not a valid uid" in str(excinfo_uid.value)

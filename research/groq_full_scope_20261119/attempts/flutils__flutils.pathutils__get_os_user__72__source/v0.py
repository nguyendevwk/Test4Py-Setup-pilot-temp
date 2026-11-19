import getpass
import os
import pwd
import pytest
from flutils.pathutils import get_os_user


def test_get_os_user_current_user_returns_struct_passwd(tmp_path):
    """Calling get_os_user with no argument should return the current user."""
    current_user = getpass.getuser()
    expected = pwd.getpwnam(current_user)
    result = get_os_user()
    assert isinstance(result, pwd.struct_passwd)
    assert result.pw_name == expected.pw_name
    assert result.pw_uid == expected.pw_uid
    assert result.pw_gid == expected.pw_gid
    assert result.pw_dir == expected.pw_dir
    assert result.pw_shell == expected.pw_shell


def test_get_os_user_with_valid_uid_returns_struct_passwd(tmp_path):
    """Providing a valid UID should return the corresponding user struct."""
    # Use the current user's UID for a guaranteed valid test
    uid = os.getuid()
    expected = pwd.getpwuid(uid)
    result = get_os_user(uid)
    assert isinstance(result, pwd.struct_passwd)
    assert result.pw_name == expected.pw_name
    assert result.pw_uid == expected.pw_uid
    assert result.pw_gid == expected.pw_gid
    assert result.pw_dir == expected.pw_dir
    assert result.pw_shell == expected.pw_shell


def test_get_os_user_invalid_name_or_uid_raises_os_error(tmp_path):
    """Providing an invalid name or UID should raise OSError."""
    # Invalid name
    with pytest.raises(OSError) as exc_name:
        get_os_user("this_user_does_not_exist_12345")
    assert "not a valid \"login name\"" in str(exc_name.value)

    # Invalid UID (negative number unlikely to exist)
    with pytest.raises(OSError) as exc_uid:
        get_os_user(-1)
    assert "not a valid uid" in str(exc_uid.value)

import getpass
import os
import pwd
import pytest
from flutils.pathutils import get_os_user


def test_get_os_user_current_user_returns_struct_passwd(tmp_path):
    """Calling get_os_user with no argument returns the current user struct."""
    current_user = getpass.getuser()
    user_struct = get_os_user()
    assert isinstance(user_struct, pwd.struct_passwd)
    assert user_struct.pw_name == current_user
    # The home directory should exist
    assert os.path.isdir(user_struct.pw_dir)


def test_get_os_user_invalid_uid_raises_os_error(tmp_path):
    """Providing a non‑existent uid raises an OSError."""
    # Choose a uid that is unlikely to exist (e.g., a very large number)
    invalid_uid = 999999
    with pytest.raises(OSError) as excinfo:
        get_os_user(invalid_uid)
    assert f"{invalid_uid}" in str(excinfo.value)
    assert "uid" in str(excinfo.value)


def test_get_os_user_invalid_name_raises_os_error(tmp_path):
    """Providing a non‑existent login name raises an OSError."""
    invalid_name = "this_user_does_not_exist_12345"
    with pytest.raises(OSError) as excinfo:
        get_os_user(invalid_name)
    assert f"{invalid_name}" in str(excinfo.value)
    assert "login name" in str(excinfo.value)

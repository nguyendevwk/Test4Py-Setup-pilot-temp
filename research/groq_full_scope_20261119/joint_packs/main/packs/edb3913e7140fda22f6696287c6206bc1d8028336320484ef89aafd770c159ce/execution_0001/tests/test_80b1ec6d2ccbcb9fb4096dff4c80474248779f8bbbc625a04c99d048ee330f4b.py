import os
import pwd
import getpass
import pytest
from flutils.pathutils import get_os_user

def test_get_os_user_current_user():
    """When no argument is given, the function returns the current user."""
    current_user = getpass.getuser()
    result = get_os_user()
    assert isinstance(result, pwd.struct_passwd)
    assert result.pw_name == current_user
    # The returned struct should match the system's record for the current user
    system_record = pwd.getpwnam(current_user)
    assert result == system_record

def test_get_os_user_by_uid():
    """When an integer uid is provided, the function returns the matching user."""
    current_user_record = pwd.getpwnam(getpass.getuser())
    uid = current_user_record.pw_uid
    result = get_os_user(uid)
    assert isinstance(result, pwd.struct_passwd)
    assert result.pw_uid == uid
    assert result.pw_name == current_user_record.pw_name

def test_get_os_user_invalid_name_and_uid():
    """Providing an invalid name or uid raises OSError."""
    # Invalid name
    with pytest.raises(OSError) as excinfo_name:
        get_os_user("__nonexistent_user__")
    assert "not a valid \"login name\"" in str(excinfo_name.value)

    # Invalid uid (negative values are not valid on most systems)
    with pytest.raises(OSError) as excinfo_uid:
        get_os_user(-1)
    assert "not a valid uid" in str(excinfo_uid.value)

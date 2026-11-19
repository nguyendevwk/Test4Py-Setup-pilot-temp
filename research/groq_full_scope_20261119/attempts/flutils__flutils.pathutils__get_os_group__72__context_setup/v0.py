import grp
import getpass
import os
import pwd
import pytest

from flutils.pathutils import get_os_group


def test_get_os_group_default_returns_current_user_group():
    """When called without arguments, get_os_group should return the
    group of the current user."""
    current_user = getpass.getuser()
    user_info = pwd.getpwnam(current_user)
    expected_gid = user_info.pw_gid
    group = get_os_group()
    assert isinstance(group, grp.struct_group)
    assert group.gr_gid == expected_gid
    # The group name should match the group name of the current user
    assert group.gr_name == grp.getgrgid(expected_gid).gr_name


def test_get_os_group_with_valid_gid_returns_correct_group():
    """Providing a valid gid should return the corresponding group."""
    # Pick the gid of the current user
    current_user = getpass.getuser()
    user_info = pwd.getpwnam(current_user)
    gid = user_info.pw_gid
    group = get_os_group(gid)
    assert isinstance(group, grp.struct_group)
    assert group.gr_gid == gid
    # The name should match the name returned by grp.getgrgid
    assert group.gr_name == grp.getgrgid(gid).gr_name


def test_get_os_group_with_invalid_name_or_gid_raises_os_error():
    """Providing an unknown group name or gid should raise OSError."""
    # Use a name that is unlikely to exist
    with pytest.raises(OSError) as excinfo_name:
        get_os_group("this_group_name_does_not_exist_12345")
    assert "not a valid \"group name\"" in str(excinfo_name.value)

    # Use a gid that is unlikely to exist (negative or very large)
    with pytest.raises(OSError) as excinfo_gid:
        get_os_group(-1)
    assert "not a valid gid" in str(excinfo_gid.value)

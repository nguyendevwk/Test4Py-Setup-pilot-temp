import grp
import getpass
import os
import pwd
import pytest

from flutils.pathutils import get_os_group


def test_get_os_group_by_name_existing():
    """Existing group name should return a grp.struct_group."""
    # Use the current user's primary group name
    current_user = getpass.getuser()
    current_gid = pwd.getpwnam(current_user).pw_gid
    group_name = grp.getgrgid(current_gid).gr_name

    group = get_os_group(group_name)
    assert isinstance(group, grp.struct_group)
    assert group.gr_gid == current_gid
    assert group.gr_name == group_name
    # The group should contain the current user
    assert current_user in group.gr_mem or current_user == group.gr_name


def test_get_os_group_by_gid_existing():
    """Existing gid should return a grp.struct_group."""
    # Use the current user's primary group gid
    current_gid = pwd.getpwnam(getpass.getuser()).pw_gid
    group = get_os_group(current_gid)
    assert isinstance(group, grp.struct_group)
    assert group.gr_gid == current_gid
    assert group.gr_name == grp.getgrgid(current_gid).gr_name


def test_get_os_group_invalid():
    """Invalid name or gid should raise OSError."""
    # Choose a name that is unlikely to exist
    invalid_name = "this_group_name_does_not_exist_12345"
    with pytest.raises(OSError) as excinfo_name:
        get_os_group(invalid_name)
    assert "not a valid \"group name\"" in str(excinfo_name.value)

    # Choose a gid that is unlikely to exist
    invalid_gid = 9999999
    with pytest.raises(OSError) as excinfo_gid:
        get_os_group(invalid_gid)
    assert "not a valid gid" in str(excinfo_gid.value)

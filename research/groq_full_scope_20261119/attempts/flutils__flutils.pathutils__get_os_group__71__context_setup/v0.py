import grp
import getpass
import os
import pwd
import pytest

from flutils.pathutils import get_os_group, get_os_user


def test_get_os_group_by_name_and_gid(tmp_path):
    """Verify that get_os_group returns the same group object when queried
    by name and by gid for the current user's primary group."""
    # Get the current user's primary group name and gid
    user = get_os_user()
    group_name = user.pw_name  # use the user name to fetch group by name
    group_obj_by_name = get_os_group(group_name)
    group_obj_by_gid = get_os_group(user.pw_gid)

    # The returned objects should be equal and have the expected attributes
    assert isinstance(group_obj_by_name, grp.struct_group)
    assert isinstance(group_obj_by_gid, grp.struct_group)
    assert group_obj_by_name.gr_name == group_obj_by_gid.gr_name
    assert group_obj_by_name.gr_gid == group_obj_by_gid.gr_gid
    assert group_obj_by_name.gr_passwd == group_obj_by_gid.gr_passwd
    assert group_obj_by_name.gr_mem == group_obj_by_gid.gr_mem


def test_get_os_group_invalid_gid_raises(tmp_path):
    """Verify that an invalid gid raises an OSError."""
    # Choose a gid that is unlikely to exist (e.g., a very large number)
    invalid_gid = 999999
    with pytest.raises(OSError) as excinfo:
        get_os_group(invalid_gid)
    assert f"{invalid_gid}" in str(excinfo.value)
    assert "gid" in str(excinfo.value).lower()


def test_get_os_group_invalid_name_raises(tmp_path):
    """Verify that an invalid group name raises an OSError."""
    # Use a name that is unlikely to exist
    invalid_name = "this_group_does_not_exist_12345"
    with pytest.raises(OSError) as excinfo:
        get_os_group(invalid_name)
    assert invalid_name in str(excinfo.value)
    assert "name" in str(excinfo.value).lower()

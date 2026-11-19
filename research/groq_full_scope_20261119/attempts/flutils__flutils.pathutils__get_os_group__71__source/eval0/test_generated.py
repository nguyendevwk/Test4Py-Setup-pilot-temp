import os
import grp
import getpass
import pytest
from flutils.pathutils import get_os_group


def test_get_os_group_current_user_group():
    """Calling get_os_group with no argument returns the current user's group."""
    current_gid = os.getgid()
    group = get_os_group()
    assert isinstance(group, grp.struct_group)
    assert group.gr_gid == current_gid
    # The group name should match the name returned by grp.getgrgid
    assert group.gr_name == grp.getgrgid(current_gid).gr_name


def test_get_os_group_by_gid_valid():
    """Providing a valid gid returns the corresponding group."""
    # Use the current gid as a valid example
    gid = os.getgid()
    group = get_os_group(gid)
    assert isinstance(group, grp.struct_group)
    assert group.gr_gid == gid
    assert group.gr_name == grp.getgrgid(gid).gr_name


def test_get_os_group_invalid_inputs():
    """Providing an invalid gid or name raises OSError with an informative message."""
    # Invalid gid
    with pytest.raises(OSError) as excinfo_gid:
        get_os_group(-1)
    assert "not a valid gid" in str(excinfo_gid.value)

    # Invalid name
    with pytest.raises(OSError) as excinfo_name:
        get_os_group("this_group_does_not_exist_12345")
    assert "not a valid \"group name\"" in str(excinfo_name.value)

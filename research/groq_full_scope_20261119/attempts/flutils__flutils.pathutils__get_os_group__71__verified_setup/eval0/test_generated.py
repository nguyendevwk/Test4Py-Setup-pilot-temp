import os
import grp
import getpass
import pytest
from flutils.pathutils import get_os_group

def test_get_os_group_by_gid_returns_correct_group():
    """When a valid gid is supplied, the returned struct_group must match the OS group."""
    current_gid = os.getgid()
    group = get_os_group(current_gid)
    assert isinstance(group, grp.struct_group)
    assert group.gr_gid == current_gid
    # The group name should be the same as the one returned by the standard library
    expected_group = grp.getgrgid(current_gid)
    assert group.gr_name == expected_group.gr_name
    assert group.gr_mem == expected_group.gr_mem

def test_get_os_group_by_name_returns_correct_group():
    """When a valid group name is supplied, the returned struct_group must match the OS group."""
    current_gid = os.getgid()
    expected_group = grp.getgrgid(current_gid)
    group = get_os_group(expected_group.gr_name)
    assert isinstance(group, grp.struct_group)
    assert group.gr_gid == expected_group.gr_gid
    assert group.gr_name == expected_group.gr_name
    assert group.gr_mem == expected_group.gr_mem

def test_get_os_group_invalid_inputs_raise_os_error():
    """Providing an unknown group name or gid should raise OSError."""
    # Unknown group name
    with pytest.raises(OSError) as exc_name:
        get_os_group("this_group_name_does_not_exist_12345")
    assert "not a valid \"group name\"" in str(exc_name.value)

    # Unknown gid (negative number unlikely to exist)
    with pytest.raises(OSError) as exc_name:
        get_os_group(-1)
    assert "not a valid gid" in str(exc_name.value)

import os
import grp
import pytest
from flutils.pathutils import get_os_group


def test_get_os_group_default_returns_current_user_group():
    """Calling get_os_group with no argument should return the current
    user's primary group."""
    current_gid = os.getgid()
    group = get_os_group()
    assert isinstance(group, grp.struct_group)
    assert group.gr_gid == current_gid
    # The group name should match the one returned by grp.getgrgid
    expected_group = grp.getgrgid(current_gid)
    assert group.gr_name == expected_group.gr_name
    assert group.gr_mem == expected_group.gr_mem


def test_get_os_group_with_existing_group_name():
    """Providing an existing group name should return the correct group."""
    # Use the current user's primary group name
    current_group = grp.getgrgid(os.getgid())
    group_name = current_group.gr_name
    group = get_os_group(group_name)
    assert isinstance(group, grp.struct_group)
    assert group.gr_name == group_name
    assert group.gr_gid == current_group.gr_gid
    assert group.gr_mem == current_group.gr_mem


def test_get_os_group_invalid_name_or_gid_raises_os_error():
    """Providing a non‑existent group name or gid should raise OSError."""
    # Non‑existent group name
    with pytest.raises(OSError) as excinfo_name:
        get_os_group("this_group_does_not_exist_12345")
    assert "not a valid \"group name\"" in str(excinfo_name.value)

    # Non‑existent gid (negative value)
    with pytest.raises(OSError) as excinfo_gid:
        get_os_group(-1)
    assert "not a valid gid" in str(excinfo_gid.value)

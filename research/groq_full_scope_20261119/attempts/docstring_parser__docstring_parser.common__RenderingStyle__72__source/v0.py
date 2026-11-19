import pytest
from docstring_parser.common import RenderingStyle


def test_rendering_style_values_and_iteration():
    # Verify that each enum member has the expected integer value
    assert RenderingStyle.COMPACT.value == 1
    assert RenderingStyle.CLEAN.value == 2
    assert RenderingStyle.EXPANDED.value == 3

    # Ensure that the enum can be iterated over and contains all members
    members = list(RenderingStyle)
    assert len(members) == 3
    assert RenderingStyle.COMPACT in members
    assert RenderingStyle.CLEAN in members
    assert RenderingStyle.EXPANDED in members


def test_access_by_name_and_member_equality():
    # Accessing by name should return the same member instance
    compact_by_name = RenderingStyle["COMPACT"]
    assert compact_by_name is RenderingStyle.COMPACT

    # Equality between members with the same value should be True
    assert RenderingStyle.COMPACT == RenderingStyle("COMPACT")
    assert RenderingStyle.CLEAN == RenderingStyle(2)

    # The enum is hashable and can be used in a set
    unique_members = {RenderingStyle.COMPACT, RenderingStyle.CLEAN, RenderingStyle.EXPANDED}
    assert len(unique_members) == 3


def test_invalid_access_raises():
    # Accessing a non-existent member by name should raise KeyError
    with pytest.raises(KeyError):
        _ = RenderingStyle["NON_EXISTENT"]

    # Creating an enum with an invalid value should raise ValueError
    with pytest.raises(ValueError):
        _ = RenderingStyle(99)

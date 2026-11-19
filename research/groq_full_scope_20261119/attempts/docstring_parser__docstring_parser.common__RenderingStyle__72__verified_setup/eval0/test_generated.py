import pytest
from docstring_parser.common import RenderingStyle


def test_rendering_style_members_and_values():
    """Verify that the enum members exist with correct values and are comparable."""
    assert RenderingStyle.COMPACT.value == 1
    assert RenderingStyle.CLEAN.value == 2
    assert RenderingStyle.EXPANDED.value == 3

    # Enum members are unique and hashable
    members = {RenderingStyle.COMPACT, RenderingStyle.CLEAN, RenderingStyle.EXPANDED}
    assert len(members) == 3
    assert RenderingStyle.COMPACT in members
    assert RenderingStyle.CLEAN in members
    assert RenderingStyle.EXPANDED in members

    # Order of iteration matches declaration order
    assert list(RenderingStyle) == [
        RenderingStyle.COMPACT,
        RenderingStyle.CLEAN,
        RenderingStyle.EXPANDED,
    ]


def test_rendering_style_from_value_and_name():
    """Test that enum can be constructed from value and name."""
    # From value
    assert RenderingStyle(1) is RenderingStyle.COMPACT
    assert RenderingStyle(2) is RenderingStyle.CLEAN
    assert RenderingStyle(3) is RenderingStyle.EXPANDED

    # From name
    assert RenderingStyle["COMPACT"] is RenderingStyle.COMPACT
    assert RenderingStyle["CLEAN"] is RenderingStyle.CLEAN
    assert RenderingStyle["EXPANDED"] is RenderingStyle.EXPANDED


def test_rendering_style_invalid_creation_raises():
    """Ensure that invalid values or names raise appropriate exceptions."""
    with pytest.raises(ValueError):
        RenderingStyle(0)  # value not defined

    with pytest.raises(ValueError):
        RenderingStyle(4)  # value not defined

    with pytest.raises(KeyError):
        RenderingStyle["UNKNOWN"]  # name not defined

import pytest
from docstring_parser.common import RenderingStyle


def test_rendering_style_members_and_values():
    """Verify that enum members exist and have correct values."""
    assert RenderingStyle.COMPACT.value == 1
    assert RenderingStyle.CLEAN.value == 2
    assert RenderingStyle.EXPANDED.value == 3
    # Ensure members are unique and hashable
    assert len({RenderingStyle.COMPACT, RenderingStyle.CLEAN, RenderingStyle.EXPANDED}) == 3
    # Check that the enum can be constructed from its value
    assert RenderingStyle(1) is RenderingStyle.COMPACT
    assert RenderingStyle(2) is RenderingStyle.CLEAN
    assert RenderingStyle(3) is RenderingStyle.EXPANDED


def test_rendering_style_iteration_and_order():
    """Ensure that iteration over the enum yields members in declaration order."""
    expected_order = [RenderingStyle.COMPACT, RenderingStyle.CLEAN, RenderingStyle.EXPANDED]
    assert list(RenderingStyle) == expected_order
    # The order should be preserved even if we access members out of order
    assert RenderingStyle.EXPANDED in RenderingStyle
    assert RenderingStyle.COMPACT in RenderingStyle
    assert RenderingStyle.CLEAN in RenderingStyle


def test_rendering_style_invalid_access_and_value():
    """Accessing a non‑existent member or invalid value should raise appropriate errors."""
    with pytest.raises(AttributeError):
        _ = RenderingStyle.NON_EXISTENT
    with pytest.raises(ValueError):
        _ = RenderingStyle(99)

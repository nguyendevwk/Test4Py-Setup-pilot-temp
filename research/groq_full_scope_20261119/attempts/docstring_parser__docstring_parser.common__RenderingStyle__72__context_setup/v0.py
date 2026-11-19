import pytest
from docstring_parser.common import RenderingStyle


def test_rendering_style_members_and_values():
    """Verify that the enum members exist with correct values and are comparable."""
    assert RenderingStyle.COMPACT.value == 1
    assert RenderingStyle.CLEAN.value == 2
    assert RenderingStyle.EXPANDED.value == 3

    # Enum members are singletons
    assert RenderingStyle.COMPACT is RenderingStyle(1)
    assert RenderingStyle.CLEAN is RenderingStyle(2)
    assert RenderingStyle.EXPANDED is RenderingStyle(3)

    # Order of iteration matches declaration order
    expected_order = [RenderingStyle.COMPACT, RenderingStyle.CLEAN, RenderingStyle.EXPANDED]
    assert list(RenderingStyle) == expected_order


def test_rendering_style_invalid_value_raises():
    """Creating an enum with an invalid value should raise ValueError."""
    with pytest.raises(ValueError) as excinfo:
        RenderingStyle(99)
    assert "99" in str(excinfo.value)
    assert "RenderingStyle" in str(excinfo.value)


def test_rendering_style_name_lookup_and_str():
    """Lookup by name works and string representation is human‑readable."""
    assert RenderingStyle["COMPACT"] is RenderingStyle.COMPACT
    assert RenderingStyle["CLEAN"] is RenderingStyle.CLEAN
    assert RenderingStyle["EXPANDED"] is RenderingStyle.EXPANDED

    # __str__ returns the name
    assert str(RenderingStyle.COMPACT) == "COMPACT"
    assert str(RenderingStyle.CLEAN) == "CLEAN"
    assert str(RenderingStyle.EXPANDED) == "EXPANDED"

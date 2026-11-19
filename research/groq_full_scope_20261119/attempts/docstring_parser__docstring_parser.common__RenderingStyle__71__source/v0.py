import pytest
from docstring_parser.common import RenderingStyle


def test_rendering_style_values():
    """Ensure enum members have correct integer values."""
    assert RenderingStyle.COMPACT.value == 1
    assert RenderingStyle.CLEAN.value == 2
    assert RenderingStyle.EXPANDED.value == 3
    # The enum should not allow duplicate values
    with pytest.raises(ValueError):
        class DuplicateStyle(RenderingStyle):
            DUPLICATE = 1


def test_rendering_style_iteration_and_membership():
    """Verify that iteration yields all members and membership checks work."""
    members = list(RenderingStyle)
    assert members == [
        RenderingStyle.COMPACT,
        RenderingStyle.CLEAN,
        RenderingStyle.EXPANDED,
    ]
    assert RenderingStyle.COMPACT in RenderingStyle
    assert RenderingStyle("COMPACT") is RenderingStyle.COMPACT
    assert RenderingStyle(2) is RenderingStyle.CLEAN
    with pytest.raises(ValueError):
        RenderingStyle("NON_EXISTENT")
    with pytest.raises(ValueError):
        RenderingStyle(99)


def test_rendering_style_comparison_and_hash():
    """Check that enum members are comparable and hashable."""
    assert RenderingStyle.COMPACT == RenderingStyle.COMPACT
    assert RenderingStyle.COMPACT != RenderingStyle.CLEAN
    assert hash(RenderingStyle.COMPACT) == hash(RenderingStyle.COMPACT)
    # Ensure they can be used as dictionary keys
    mapping = {RenderingStyle.COMPACT: "compact", RenderingStyle.CLEAN: "clean"}
    assert mapping[RenderingStyle.COMPACT] == "compact"
    assert mapping[RenderingStyle.CLEAN] == "clean"

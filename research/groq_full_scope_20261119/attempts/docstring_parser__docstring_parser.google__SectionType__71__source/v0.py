import pytest
from docstring_parser.google import SectionType


def test_section_type_values_and_names():
    """SectionType should expose the correct names and integer values."""
    assert SectionType.SINGULAR.value == 0
    assert SectionType.MULTIPLE.value == 1
    assert SectionType.SINGULAR_OR_MULTIPLE.value == 2
    assert SectionType(0) is SectionType.SINGULAR
    assert SectionType(1) is SectionType.MULTIPLE
    assert SectionType(2) is SectionType.SINGULAR_OR_MULTIPLE
    # Ensure the enum is iterable and contains exactly the three members
    members = list(SectionType)
    assert len(members) == 3
    assert set(m.name for m in members) == {"SINGULAR", "MULTIPLE", "SINGULAR_OR_MULTIPLE"}


def test_section_type_invalid_value_raises():
    """Creating a SectionType with an invalid integer should raise ValueError."""
    with pytest.raises(ValueError):
        SectionType(3)
    with pytest.raises(ValueError):
        SectionType(-1)
    with pytest.raises(ValueError):
        SectionType("invalid")  # type: ignore[arg-type]


def test_section_type_int_enum_behavior():
    """SectionType should behave like a normal IntEnum: comparison and hashing."""
    assert SectionType.SINGULAR == 0
    assert SectionType.MULTIPLE == 1
    assert SectionType.SINGULAR_OR_MULTIPLE == 2
    # Hashing should be consistent with the integer value
    assert hash(SectionType.SINGULAR) == hash(0)
    assert hash(SectionType.MULTIPLE) == hash(1)
    assert hash(SectionType.SINGULAR_OR_MULTIPLE) == hash(2)
    # Equality with other enum members
    assert SectionType.SINGULAR != SectionType.MULTIPLE
    assert SectionType.SINGULAR != SectionType.SINGULAR_OR_MULTIPLE
    assert SectionType.MULTIPLE != SectionType.SINGULAR_OR_MULTIPLE

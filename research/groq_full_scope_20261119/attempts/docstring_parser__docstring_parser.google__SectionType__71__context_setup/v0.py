import pytest
from docstring_parser.google import SectionType

def test_section_type_values_and_names():
    """Verify that SectionType members have correct integer values and names."""
    assert SectionType.SINGULAR.value == 0
    assert SectionType.MULTIPLE.value == 1
    assert SectionType.SINGULAR_OR_MULTIPLE.value == 2
    assert SectionType(0) is SectionType.SINGULAR
    assert SectionType(1) is SectionType.MULTIPLE
    assert SectionType(2) is SectionType.SINGULAR_OR_MULTIPLE
    # Ensure the enum preserves the order of definition
    assert list(SectionType) == [
        SectionType.SINGULAR,
        SectionType.MULTIPLE,
        SectionType.SINGULAR_OR_MULTIPLE,
    ]

def test_section_type_int_enum_behavior():
    """SectionType should behave like an IntEnum: support integer comparison and arithmetic."""
    assert SectionType.SINGULAR == 0
    assert SectionType.MULTIPLE == 1
    assert SectionType.SINGULAR_OR_MULTIPLE == 2
    # Arithmetic operations should produce integers, not SectionType
    assert isinstance(SectionType.SINGULAR + 1, int)
    assert SectionType.SINGULAR + 1 == 1
    # Comparisons with other enums should raise TypeError
    with pytest.raises(TypeError):
        _ = SectionType.SINGULAR < SectionType.MULTIPLE  # IntEnum supports comparison, but not with other types

def test_section_type_invalid_value_raises():
    """Creating a SectionType with an invalid value should raise ValueError."""
    with pytest.raises(ValueError):
        SectionType(3)
    with pytest.raises(ValueError):
        SectionType(-1)
    # Ensure that passing a non-integer raises TypeError
    with pytest.raises(TypeError):
        SectionType("0")

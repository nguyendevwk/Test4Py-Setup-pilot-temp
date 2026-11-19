import pytest
from docstring_parser.google import SectionType

def test_section_type_members_and_values():
    # Verify that each enum member has the expected integer value
    assert SectionType.SINGULAR.value == 0
    assert SectionType.MULTIPLE.value == 1
    assert SectionType.SINGULAR_OR_MULTIPLE.value == 2
    # Verify that the names are correct
    assert SectionType(0).name == "SINGULAR"
    assert SectionType(1).name == "MULTIPLE"
    assert SectionType(2).name == "SINGULAR_OR_MULTIPLE"
    # Ensure that the enum is iterable and contains all members
    names = {member.name for member in SectionType}
    assert names == {"SINGULAR", "MULTIPLE", "SINGULAR_OR_MULTIPLE"}

def test_section_type_int_conversion_and_lookup():
    # Converting an enum member to int yields its value
    assert int(SectionType.SINGULAR) == 0
    assert int(SectionType.MULTIPLE) == 1
    assert int(SectionType.SINGULAR_OR_MULTIPLE) == 2
    # Looking up by integer returns the correct member
    assert SectionType(0) is SectionType.SINGULAR
    assert SectionType(1) is SectionType.MULTIPLE
    assert SectionType(2) is SectionType.SINGULAR_OR_MULTIPLE
    # The enum supports reverse lookup via the value
    assert SectionType(SectionType.SINGULAR.value) is SectionType.SINGULAR

def test_section_type_invalid_value_raises():
    # Passing an integer that is not a valid enum value should raise ValueError
    with pytest.raises(ValueError):
        SectionType(3)
    # Passing a non-integer type should also raise ValueError
    with pytest.raises(ValueError):
        SectionType("invalid")

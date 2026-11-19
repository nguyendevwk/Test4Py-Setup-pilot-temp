import pytest
from docstring_parser.google import SectionType

def test_section_type_values_and_names():
    # Verify that the enum members have the expected integer values
    assert SectionType.SINGULAR.value == 0
    assert SectionType.MULTIPLE.value == 1
    assert SectionType.SINGULAR_OR_MULTIPLE.value == 2

    # Verify that the enum members have the expected names
    assert SectionType(0).name == "SINGULAR"
    assert SectionType(1).name == "MULTIPLE"
    assert SectionType(2).name == "SINGULAR_OR_MULTIPLE"

def test_section_type_iteration_and_members():
    # The enum should contain exactly three members
    members = list(SectionType)
    assert len(members) == 3
    names = {member.name for member in members}
    assert names == {"SINGULAR", "MULTIPLE", "SINGULAR_OR_MULTIPLE"}

    # Each member should be an instance of SectionType
    for member in members:
        assert isinstance(member, SectionType)

def test_section_type_invalid_value_raises():
    # Accessing an undefined integer value should raise a ValueError
    with pytest.raises(ValueError):
        SectionType(3)
    with pytest.raises(ValueError):
        SectionType(-1)

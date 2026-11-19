import pytest
from docstring_parser.google import SectionType


def test_section_type_members_and_values():
    """Verify that the enum members exist and have the expected integer values."""
    assert SectionType.SINGULAR.value == 0
    assert SectionType.MULTIPLE.value == 1
    assert SectionType.SINGULAR_OR_MULTIPLE.value == 2
    # Ensure the members are instances of IntEnum
    assert isinstance(SectionType.SINGULAR, SectionType)
    assert isinstance(SectionType.MULTIPLE, SectionType)
    assert isinstance(SectionType.SINGULAR_OR_MULTIPLE, SectionType)
    # The enum should contain exactly three members
    assert set(SectionType) == {
        SectionType.SINGULAR,
        SectionType.MULTIPLE,
        SectionType.SINGULAR_OR_MULTIPLE,
    }


def test_section_type_lookup_and_comparison(tmp_path):
    """Test that SectionType can be constructed from an integer and compared correctly."""
    # Construction from integer
    singular = SectionType(0)
    multiple = SectionType(1)
    singular_or_multiple = SectionType(2)
    assert singular is SectionType.SINGULAR
    assert multiple is SectionType.MULTIPLE
    assert singular_or_multiple is SectionType.SINGULAR_OR_MULTIPLE

    # Comparison and ordering
    assert singular < multiple < singular_or_multiple
    assert singular != multiple
    assert multiple == SectionType.MULTIPLE

    # Use as dictionary keys
    mapping = {SectionType.SINGULAR: "single", SectionType.MULTIPLE: "multiple"}
    assert mapping[SectionType.SINGULAR] == "single"
    assert mapping[SectionType.MULTIPLE] == "multiple"

    # Persist the enum value to a file and read it back
    file_path = tmp_path / "section_type.txt"
    file_path.write_text(str(singular.value))
    read_value = int(file_path.read_text())
    assert read_value == 0
    assert SectionType(read_value) is SectionType.SINGULAR


def test_section_type_invalid_value():
    """Ensure that constructing SectionType with an invalid value raises ValueError."""
    with pytest.raises(ValueError):
        SectionType(3)
    with pytest.raises(ValueError):
        SectionType(-1)
    with pytest.raises(ValueError):
        SectionType(999)

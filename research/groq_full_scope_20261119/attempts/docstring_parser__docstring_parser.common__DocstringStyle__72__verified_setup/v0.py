import pytest
from docstring_parser.common import DocstringStyle


def test_enum_members_and_values():
    """Verify that each enum member has the expected integer value."""
    assert DocstringStyle.REST.value == 1
    assert DocstringStyle.GOOGLE.value == 2
    assert DocstringStyle.NUMPYDOC.value == 3
    assert DocstringStyle.EPYDOC.value == 4
    assert DocstringStyle.AUTO.value == 255
    # Ensure the names match the enum definition
    assert DocstringStyle(1).name == "REST"
    assert DocstringStyle(2).name == "GOOGLE"
    assert DocstringStyle(3).name == "NUMPYDOC"
    assert DocstringStyle(4).name == "EPYDOC"
    assert DocstringStyle(255).name == "AUTO"


def test_enum_lookup_by_value_and_name():
    """Test that enum can be accessed by both value and name."""
    # Lookup by value
    rest = DocstringStyle(1)
    google = DocstringStyle(2)
    # Lookup by name
    assert DocstringStyle["REST"] is rest
    assert DocstringStyle["GOOGLE"] is google
    # Ensure that the same instance is returned for repeated lookups
    assert DocstringStyle(1) is DocstringStyle.REST
    assert DocstringStyle("NUMPYDOC") is DocstringStyle.NUMPYDOC


def test_invalid_enum_value_raises():
    """Accessing an undefined enum value should raise ValueError."""
    with pytest.raises(ValueError):
        DocstringStyle(999)
    with pytest.raises(ValueError):
        DocstringStyle("INVALID_NAME")

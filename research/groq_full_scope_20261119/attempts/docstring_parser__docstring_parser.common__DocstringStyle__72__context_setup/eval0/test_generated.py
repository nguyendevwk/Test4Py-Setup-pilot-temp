import pytest
from docstring_parser.common import DocstringStyle


def test_enum_members_and_values():
    """Verify that each enum member has the expected integer value."""
    assert DocstringStyle.REST.value == 1
    assert DocstringStyle.GOOGLE.value == 2
    assert DocstringStyle.NUMPYDOC.value == 3
    assert DocstringStyle.EPYDOC.value == 4
    assert DocstringStyle.AUTO.value == 255
    # Ensure the names are correct
    assert DocstringStyle(1).name == "REST"
    assert DocstringStyle(2).name == "GOOGLE"
    assert DocstringStyle(3).name == "NUMPYDOC"
    assert DocstringStyle(4).name == "EPYDOC"
    assert DocstringStyle(255).name == "AUTO"


def test_enum_lookup_by_value_and_name():
    """Test that enum can be accessed by both value and name."""
    # Lookup by value
    assert DocstringStyle(1) is DocstringStyle.REST
    assert DocstringStyle(255) is DocstringStyle.AUTO
    # Lookup by name
    assert DocstringStyle["GOOGLE"] is DocstringStyle.GOOGLE
    assert DocstringStyle["NUMPYDOC"] is DocstringStyle.NUMPYDOC


def test_enum_invalid_value_raises():
    """Accessing an undefined value should raise ValueError."""
    with pytest.raises(ValueError):
        DocstringStyle(999)

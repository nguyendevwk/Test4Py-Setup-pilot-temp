import pytest
from docstring_parser.common import DocstringStyle


def test_docstring_style_members_and_values():
    """Verify that each enum member exists and has the expected integer value."""
    assert DocstringStyle.REST.value == 1
    assert DocstringStyle.GOOGLE.value == 2
    assert DocstringStyle.NUMPYDOC.value == 3
    assert DocstringStyle.EPYDOC.value == 4
    assert DocstringStyle.AUTO.value == 255
    # Ensure the enum is iterable and contains all members
    names = {member.name for member in DocstringStyle}
    assert names == {"REST", "GOOGLE", "NUMPYDOC", "EPYDOC", "AUTO"}


def test_docstring_style_lookup_by_value_and_name():
    """Test that enum members can be accessed by value and name."""
    # Lookup by value
    assert DocstringStyle(1) is DocstringStyle.REST
    assert DocstringStyle(2) is DocstringStyle.GOOGLE
    assert DocstringStyle(3) is DocstringStyle.NUMPYDOC
    assert DocstringStyle(4) is DocstringStyle.EPYDOC
    assert DocstringStyle(255) is DocstringStyle.AUTO
    # Lookup by name
    assert DocstringStyle["REST"] is DocstringStyle.REST
    assert DocstringStyle["GOOGLE"] is DocstringStyle.GOOGLE
    assert DocstringStyle["NUMPYDOC"] is DocstringStyle.NUMPYDOC
    assert DocstringStyle["EPYDOC"] is DocstringStyle.EPYDOC
    assert DocstringStyle["AUTO"] is DocstringStyle.AUTO


def test_docstring_style_invalid_value_raises():
    """Ensure that creating an enum with an invalid value raises ValueError."""
    with pytest.raises(ValueError):
        DocstringStyle(0)  # below defined range
    with pytest.raises(ValueError):
        DocstringStyle(256)  # above defined range
    with pytest.raises(ValueError):
        DocstringStyle("REST")  # wrong type

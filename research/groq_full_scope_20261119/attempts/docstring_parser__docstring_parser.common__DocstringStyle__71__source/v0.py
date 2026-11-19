import pytest
import enum
from docstring_parser.common import DocstringStyle

def test_docstring_style_members_and_values():
    # Verify that each enum member exists with the correct integer value
    assert DocstringStyle.REST.value == 1
    assert DocstringStyle.GOOGLE.value == 2
    assert DocstringStyle.NUMPYDOC.value == 3
    assert DocstringStyle.EPYDOC.value == 4
    assert DocstringStyle.AUTO.value == 255
    # Ensure the enum is iterable and contains exactly the expected members
    expected_names = {"REST", "GOOGLE", "NUMPYDOC", "EPYDOC", "AUTO"}
    assert set(member.name for member in DocstringStyle) == expected_names

def test_docstring_style_reverse_lookup_and_identity():
    # Reverse lookup by value should return the correct member
    assert DocstringStyle(1) is DocstringStyle.REST
    assert DocstringStyle(2) is DocstringStyle.GOOGLE
    assert DocstringStyle(3) is DocstringStyle.NUMPYDOC
    assert DocstringStyle(4) is DocstringStyle.EPYDOC
    assert DocstringStyle(255) is DocstringStyle.AUTO
    # Identity: comparing two members with the same value yields True
    assert DocstringStyle.REST == DocstringStyle(1)
    assert DocstringStyle.AUTO == DocstringStyle(255)

def test_docstring_style_invalid_value_raises():
    # Passing an integer not defined in the enum should raise ValueError
    with pytest.raises(ValueError):
        DocstringStyle(0)
    with pytest.raises(ValueError):
        DocstringStyle(5)
    with pytest.raises(ValueError):
        DocstringStyle(256)

import pytest
from docstring_parser.common import DocstringStyle

def test_enum_members_and_values():
    # Verify that each enum member exists and has the expected integer value
    assert DocstringStyle.REST.value == 1
    assert DocstringStyle.GOOGLE.value == 2
    assert DocstringStyle.NUMPYDOC.value == 3
    assert DocstringStyle.EPYDOC.value == 4
    assert DocstringStyle.AUTO.value == 255
    # Ensure the enum members are unique and hashable
    assert len(set(DocstringStyle)) == 5
    assert DocstringStyle.REST in DocstringStyle
    assert DocstringStyle.AUTO in DocstringStyle

def test_enum_lookup_and_iteration():
    # Lookup by name and by value should return the same member
    assert DocstringStyle['REST'] is DocstringStyle.REST
    assert DocstringStyle(1) is DocstringStyle.REST
    # Iteration over the enum yields all members in definition order
    names = [member.name for member in DocstringStyle]
    assert names == ['REST', 'GOOGLE', 'NUMPYDOC', 'EPYDOC', 'AUTO']

def test_invalid_enum_creation_raises():
    # Creating an enum member with an undefined value should raise ValueError
    with pytest.raises(ValueError):
        DocstringStyle(999)
    # Similarly, accessing a non-existent name should raise KeyError
    with pytest.raises(KeyError):
        DocstringStyle['UNKNOWN']

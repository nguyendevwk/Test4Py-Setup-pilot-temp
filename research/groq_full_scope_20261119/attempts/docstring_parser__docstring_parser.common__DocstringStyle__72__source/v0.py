import pytest
from docstring_parser.common import DocstringStyle


def test_enum_members_and_values():
    """Verify that each enum member has the expected integer value."""
    assert DocstringStyle.REST.value == 1
    assert DocstringStyle.GOOGLE.value == 2
    assert DocstringStyle.NUMPYDOC.value == 3
    assert DocstringStyle.EPYDOC.value == 4
    assert DocstringStyle.AUTO.value == 255
    # Ensure the members are unique
    values = {member.value for member in DocstringStyle}
    assert len(values) == len(DocstringStyle)


def test_lookup_by_value_and_name():
    """Check that enum can be accessed by integer value and by name."""
    assert DocstringStyle(1) is DocstringStyle.REST
    assert DocstringStyle(2) is DocstringStyle.GOOGLE
    assert DocstringStyle(3) is DocstringStyle.NUMPYDOC
    assert DocstringStyle(4) is DocstringStyle.EPYDOC
    assert DocstringStyle(255) is DocstringStyle.AUTO

    assert DocstringStyle['REST'] is DocstringStyle.REST
    assert DocstringStyle['GOOGLE'] is DocstringStyle.GOOGLE
    assert DocstringStyle['NUMPYDOC'] is DocstringStyle.NUMPYDOC
    assert DocstringStyle['EPYDOC'] is DocstringStyle.EPYDOC
    assert DocstringStyle['AUTO'] is DocstringStyle.AUTO


def test_invalid_value_raises():
    """Accessing an undefined integer value should raise ValueError."""
    with pytest.raises(ValueError):
        DocstringStyle(0)
    with pytest.raises(ValueError):
        DocstringStyle(256)
    with pytest.raises(ValueError):
        DocstringStyle(-1)

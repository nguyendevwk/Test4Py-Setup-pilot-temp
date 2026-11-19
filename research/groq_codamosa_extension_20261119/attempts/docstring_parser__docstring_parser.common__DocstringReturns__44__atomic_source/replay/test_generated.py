import pytest
from docstring_parser.common import DocstringReturns

def test_docstring_returns_basic_attributes():
    """Verify that basic attributes are stored correctly."""
    args = ["param1", "param2"]
    description = "This function returns something."
    type_name = "int"
    is_generator = False
    return_name = "result"

    dr = DocstringReturns(args, description, type_name, is_generator, return_name)

    assert dr.args == args
    assert dr.description == description
    assert dr.type_name == type_name
    assert dr.is_generator is is_generator
    assert dr.return_name == return_name

def test_docstring_returns_with_missing_optional_values():
    """Ensure optional parameters default to None when omitted."""
    args = ["x"]
    description = None
    type_name = None
    is_generator = True

    dr = DocstringReturns(args, description, type_name, is_generator)

    assert dr.args == args
    assert dr.description is None
    assert dr.type_name is None
    assert dr.is_generator is True
    assert dr.return_name is None

def test_docstring_returns_type_and_generator_flags():
    """Check that type_name and is_generator flags are independent."""
    args = []
    description = "Yielding values."
    type_name = "float"
    is_generator = True
    return_name = None

    dr = DocstringReturns(args, description, type_name, is_generator, return_name)

    assert isinstance(dr.type_name, str) and dr.type_name == "float"
    assert dr.is_generator is True
    assert dr.return_name is None

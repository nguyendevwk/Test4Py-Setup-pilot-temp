import pytest
from docstring_parser.common import DocstringReturns

def test_basic_initialization():
    """Verify that a DocstringReturns instance stores all provided values."""
    args = ["param1", "param2"]
    description = "Returns a tuple of values."
    type_name = "Tuple[int, str]"
    is_generator = True
    return_name = "result"

    dr = DocstringReturns(args, description, type_name, is_generator, return_name)

    assert dr.args == args
    assert dr.description == description
    assert dr.type_name == type_name
    assert dr.is_generator is True
    assert dr.return_name == return_name

def test_optional_return_name_and_type():
    """Check that optional fields can be omitted and default to None."""
    args = ["value"]
    description = None
    type_name = None
    is_generator = False

    dr = DocstringReturns(args, description, type_name, is_generator)

    assert dr.args == args
    assert dr.description is None
    assert dr.type_name is None
    assert dr.is_generator is False
    assert dr.return_name is None

def test_empty_args_and_boundary_values():
    """Ensure that empty args list and boundary boolean values are handled."""
    args = []
    description = ""
    type_name = ""
    is_generator = False

    dr = DocstringReturns(args, description, type_name, is_generator)

    assert dr.args == []
    assert dr.description == ""
    assert dr.type_name == ""
    assert dr.is_generator is False
    assert dr.return_name is None

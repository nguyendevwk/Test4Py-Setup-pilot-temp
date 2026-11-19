import pytest
from docstring_parser.common import DocstringReturns


def test_docstringreturns_basic():
    """Verify that a DocstringReturns instance stores the provided metadata."""
    args = ["x", "y"]
    description = "Returns the sum."
    type_name = "int"
    is_generator = False

    dr = DocstringReturns(args, description, type_name, is_generator)

    assert dr.args == args
    assert dr.description == description
    assert dr.type_name == type_name
    assert dr.is_generator is is_generator
    assert dr.return_name is None


def test_docstringreturns_with_return_name():
    """Verify that the optional return_name parameter is stored correctly."""
    args = ["value"]
    description = "Yields a value."
    type_name = "float"
    is_generator = True
    return_name = "result"

    dr = DocstringReturns(args, description, type_name, is_generator, return_name)

    assert dr.return_name == return_name
    assert dr.is_generator is True
    assert dr.type_name == type_name
    assert dr.args == args
    assert dr.description == description


def test_docstringreturns_invalid_args_type():
    """Passing a non-list to args should raise a TypeError."""
    with pytest.raises(TypeError):
        DocstringReturns("not-a-list", "desc", None, False)

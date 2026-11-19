import pytest
from docstring_parser.common import DocstringReturns

def test_normal_initialization():
    """Verify that a normal DocstringReturns instance stores all attributes correctly."""
    args = ["x", "y"]
    description = "Returns the sum."
    type_name = "int"
    is_generator = False
    return_name = "result"

    dr = DocstringReturns(args, description, type_name, is_generator, return_name)

    assert dr.args == args
    assert dr.description == description
    assert dr.type_name == type_name
    assert dr.is_generator is is_generator
    assert dr.return_name == return_name

def test_boundary_empty_and_none():
    """Test boundary conditions: empty args list and None values for optional fields."""
    dr = DocstringReturns([], None, None, True)

    assert dr.args == []
    assert dr.description is None
    assert dr.type_name is None
    assert dr.is_generator is True
    assert dr.return_name is None

def test_error_non_iterable_args():
    """Passing a non-iterable for args should raise a TypeError."""
    with pytest.raises(TypeError):
        # args should be a list; passing a string should trigger a TypeError
        DocstringReturns("not a list", "desc", "type", False)

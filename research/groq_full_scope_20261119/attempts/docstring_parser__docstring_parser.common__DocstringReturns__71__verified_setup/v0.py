import pytest
from docstring_parser.common import DocstringReturns


def test_docstring_returns_normal():
    """Normal construction with all parameters."""
    args = ["param1", "param2"]
    description = "Return value description."
    type_name = "int"
    is_generator = True
    return_name = "result"

    dr = DocstringReturns(args, description, type_name, is_generator, return_name)

    assert dr.args == args
    assert dr.description == description
    assert dr.type_name == type_name
    assert dr.is_generator is True
    assert dr.return_name == return_name


def test_docstring_returns_boundary_empty_args():
    """Construction with empty args list and None values."""
    dr = DocstringReturns([], None, None, False)

    assert dr.args == []
    assert dr.description is None
    assert dr.type_name is None
    assert dr.is_generator is False
    assert dr.return_name is None


def test_docstring_returns_invalid_args_type():
    """Construction should raise TypeError when args is not a list."""
    with pytest.raises(TypeError):
        # Passing a string instead of a list should trigger a TypeError
        DocstringReturns("not a list", "desc", "type", False)

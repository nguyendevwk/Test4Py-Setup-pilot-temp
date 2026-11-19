import pytest
from docstring_parser.common import DocstringReturns, DocstringMeta


def test_docstring_returns_basic_attributes(tmp_path):
    """Verify that DocstringReturns stores all provided arguments correctly."""
    args = ["param1", "param2"]
    description = "This function returns a value."
    type_name = "int"
    is_generator = False
    return_name = "result"

    dr = DocstringReturns(args, description, type_name, is_generator, return_name)

    # Basic attribute checks
    assert isinstance(dr, DocstringMeta)
    assert dr.args == args
    assert dr.description == description
    assert dr.type_name == type_name
    assert dr.is_generator is is_generator
    assert dr.return_name == return_name


def test_docstring_returns_with_none_and_empty(tmp_path):
    """Test boundary conditions: empty args list and None values."""
    dr = DocstringReturns([], None, None, True)

    # Empty args list should be stored as empty list
    assert dr.args == []
    # None values should be stored as None
    assert dr.description is None
    assert dr.type_name is None
    assert dr.is_generator is True
    assert dr.return_name is None


def test_docstring_returns_invalid_args_type(tmp_path):
    """Passing a non-list to args should raise a TypeError."""
    with pytest.raises(TypeError):
        # args must be a list; passing a string should trigger a TypeError
        DocstringReturns("not a list", "desc", "str", False)

import pytest
from docstring_parser.common import DocstringReturns, DocstringMeta


def test_docstring_returns_initialization_basic():
    """Verify that DocstringReturns stores basic attributes correctly."""
    args = ["x", "y"]
    description = "Return value description."
    type_name = "int"
    is_generator = False

    dr = DocstringReturns(args, description, type_name, is_generator)

    # Base class attributes
    assert isinstance(dr, DocstringMeta)
    assert dr.args == args
    assert dr.description == description

    # Specific attributes
    assert dr.type_name == type_name
    assert dr.is_generator is is_generator
    assert dr.return_name is None


def test_docstring_returns_with_return_name_and_generator():
    """Test initialization when return_name is provided and is_generator is True."""
    args = ["value"]
    description = "Yields a value."
    type_name = "float"
    is_generator = True
    return_name = "result"

    dr = DocstringReturns(args, description, type_name, is_generator, return_name)

    assert dr.args == args
    assert dr.description == description
    assert dr.type_name == type_name
    assert dr.is_generator is is_generator
    assert dr.return_name == return_name


def test_docstring_returns_invalid_types_raises_type_error(tmp_path):
    """Ensure that passing non-list args raises a TypeError."""
    # args must be a list; passing a string should raise
    with pytest.raises(TypeError):
        DocstringReturns("not a list", None, None, False)

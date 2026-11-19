import pytest
from docstring_parser.common import DocstringReturns, DocstringMeta


def test_docstring_returns_normal():
    """Verify that a normal DocstringReturns instance stores all attributes correctly."""
    args = ["param1", "param2"]
    description = "Returns a value."
    type_name = "int"
    is_generator = False
    return_name = "result"

    dr = DocstringReturns(args, description, type_name, is_generator, return_name)

    # Base class attributes
    assert isinstance(dr, DocstringMeta)
    assert dr.args == args
    assert dr.description == description

    # Specific attributes
    assert dr.type_name == type_name
    assert dr.is_generator is is_generator
    assert dr.return_name == return_name


def test_docstring_returns_boundary_empty_and_none():
    """Test boundary conditions: empty args list and None values for optional fields."""
    dr = DocstringReturns([], None, None, True)

    # Base class attributes
    assert dr.args == []
    assert dr.description is None

    # Specific attributes
    assert dr.type_name is None
    assert dr.is_generator is True
    assert dr.return_name is None


def test_docstring_returns_missing_required_arguments():
    """Ensure that missing required positional arguments raise a TypeError."""
    with pytest.raises(TypeError):
        # Missing the 'args' argument
        DocstringReturns(description="Missing args", type_name="str", is_generator=False)

    with pytest.raises(TypeError):
        # Missing 'description' argument
        DocstringReturns([], type_name="str", is_generator=False)

    with pytest.raises(TypeError):
        # Missing 'type_name' argument
        DocstringReturns([], "desc", is_generator=False)

    with pytest.raises(TypeError):
        # Missing 'is_generator' argument
        DocstringReturns([], "desc", "str")

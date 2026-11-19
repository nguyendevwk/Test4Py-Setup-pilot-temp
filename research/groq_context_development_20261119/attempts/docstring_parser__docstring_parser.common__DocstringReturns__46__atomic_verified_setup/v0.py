import pytest
from docstring_parser.common import DocstringReturns, DocstringMeta


def test_docstring_returns_basic_initialization():
    """Verify that a DocstringReturns instance stores all provided values correctly."""
    args = ["value"]
    description = "A simple return description."
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


def test_docstring_returns_with_empty_and_none_values():
    """Test initialization when optional fields are omitted or empty."""
    dr = DocstringReturns([], None, None, True)

    # Base class attributes
    assert dr.args == []
    assert dr.description is None

    # Specific attributes
    assert dr.type_name is None
    assert dr.is_generator is True
    assert dr.return_name is None


def test_docstring_returns_type_consistency_and_mutability():
    """Ensure that the instance attributes are independent copies and can be mutated."""
    original_args = ["original"]
    dr = DocstringReturns(original_args, "desc", "str", False)

    # Mutate the original list after initialization
    original_args.append("modified")
    # The instance should not reflect this change
    assert dr.args == ["original"]

    # Mutate the instance's args list
    dr.args.append("new")
    assert dr.args == ["original", "new"]
    # Ensure the original list remains unchanged
    assert original_args == ["original", "modified"]

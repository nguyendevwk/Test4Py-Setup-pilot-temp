import pytest
from docstring_parser.common import DocstringRaises


def test_docstringraises_basic():
    """Verify that a normal DocstringRaises instance stores all provided values."""
    args = ["ValueError", "TypeError"]
    description = "Raises when input is invalid."
    type_name = "ValueError"
    raises = DocstringRaises(args=args, description=description, type_name=type_name)

    # Check that the instance holds the exact values passed
    assert raises.args == args
    assert raises.description == description
    assert raises.type_name == type_name

    # Ensure that the instance is of the expected type
    assert isinstance(raises, DocstringRaises)


def test_docstringraises_none_description():
    """Verify that passing None for description is handled correctly."""
    args = ["RuntimeError"]
    description = None
    type_name = "RuntimeError"
    raises = DocstringRaises(args=args, description=description, type_name=type_name)

    # description should be stored as None
    assert raises.description is None
    # args and type_name should be stored correctly
    assert raises.args == args
    assert raises.type_name == type_name


def test_docstringraises_empty_args():
    """Verify that an empty args list is accepted and stored."""
    args = []
    description = "No specific exception types."
    type_name = None
    raises = DocstringRaises(args=args, description=description, type_name=type_name)

    # args should be an empty list
    assert raises.args == []
    # description and type_name should be stored as provided
    assert raises.description == description
    assert raises.type_name is None

import pytest
from docstring_parser.common import DocstringRaises, DocstringMeta


def test_docstringraises_basic_attributes():
    """Verify that DocstringRaises stores args, description, and type_name correctly."""
    args = ["ValueError", "TypeError"]
    description = "An error occurred."
    type_name = "ValueError"
    raises = DocstringRaises(args, description, type_name)

    # Check that the attributes are set to the exact values passed
    assert raises.args == args
    assert raises.description == description
    assert raises.type_name == type_name


def test_docstringraises_with_none_values():
    """DocstringRaises should accept None for optional fields without raising."""
    raises = DocstringRaises([], None, None)

    # The attributes should reflect the None values
    assert raises.args == []
    assert raises.description is None
    assert raises.type_name is None


def test_docstringraises_inherits_from_docstringmeta():
    """Ensure that DocstringRaises is a subclass of DocstringMeta and behaves accordingly."""
    args = ["KeyError"]
    description = "Missing key."
    type_name = "KeyError"
    raises = DocstringRaises(args, description, type_name)

    # DocstringRaises should be an instance of DocstringMeta
    assert isinstance(raises, DocstringMeta)

    # The base class should have stored the args and description
    assert raises.args == args
    assert raises.description == description

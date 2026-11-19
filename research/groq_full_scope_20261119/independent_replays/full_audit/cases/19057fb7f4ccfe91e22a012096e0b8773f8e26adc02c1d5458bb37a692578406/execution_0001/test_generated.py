import pytest
from docstring_parser.common import DocstringRaises, DocstringMeta

def test_docstringraises_initialization_basic():
    """Verify that DocstringRaises correctly stores args, description, and type_name."""
    args = ["value"]
    description = "An error occurs."
    type_name = "ValueError"
    raises = DocstringRaises(args, description, type_name)

    # Check that the instance is a subclass of DocstringMeta
    assert isinstance(raises, DocstringMeta)

    # Verify that the attributes are set as expected
    assert raises.args == args
    assert raises.description == description
    assert raises.type_name == type_name

def test_docstringraises_empty_args_and_none_description():
    """Test boundary case with empty args list and None description."""
    raises = DocstringRaises([], None, "RuntimeError")

    # Args should be an empty list
    assert raises.args == []

    # Description should be None
    assert raises.description is None

    # Type name should be stored correctly
    assert raises.type_name == "RuntimeError"

def test_docstringraises_type_name_none_and_description_override():
    """Ensure that type_name can be None and that description is overridden correctly."""
    raises = DocstringRaises(["param"], "Initial description", None)

    # Type name should be None
    assert raises.type_name is None

    # Description should be the provided string, not None
    assert raises.description == "Initial description"

    # Changing the description after initialization should not affect the stored value
    raises.description = "New description"
    assert raises.description == "New description"

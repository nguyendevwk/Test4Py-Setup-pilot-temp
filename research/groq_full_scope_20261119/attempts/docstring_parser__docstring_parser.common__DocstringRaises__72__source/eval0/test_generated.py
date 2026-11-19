import pytest
from docstring_parser.common import DocstringRaises

def test_docstringraises_basic_attributes():
    """Verify that the basic attributes are stored correctly."""
    args = ["ValueError", "TypeError"]
    description = "An error occurred."
    type_name = "ValueError"
    raises = DocstringRaises(args, description, type_name)

    # The args list should be stored unchanged
    assert raises.args == args
    # The description should be stored
    assert raises.description == description
    # The type_name should be stored
    assert raises.type_name == type_name

def test_docstringraises_with_none_and_empty_args():
    """Test handling of None description and empty args list."""
    args = []
    description = None
    type_name = None
    raises = DocstringRaises(args, description, type_name)

    # Empty args list should be preserved
    assert raises.args == []
    # None description should be stored as None
    assert raises.description is None
    # None type_name should be stored as None
    assert raises.type_name is None

def test_docstringraises_invalid_initialization():
    """Ensure that passing non-list to args raises a TypeError."""
    with pytest.raises(TypeError):
        # args must be a list; passing a string should raise
        DocstringRaises("ValueError", "desc", "ValueError")

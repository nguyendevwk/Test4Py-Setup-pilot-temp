import pytest
from docstring_parser.common import DocstringRaises, DocstringMeta

def test_docstringraises_initialization_basic():
    """Verify that DocstringRaises stores its arguments correctly."""
    args = ["param1", "param2"]
    description = "An error occurs when ..."
    type_name = "ValueError"

    meta = DocstringRaises(args, description, type_name)

    # The base class should store the args and description
    assert isinstance(meta, DocstringMeta)
    assert meta.args == args
    assert meta.description == description

    # The subclass should store the type_name
    assert meta.type_name == type_name

def test_docstringraises_handles_none_and_empty():
    """Test that None and empty values are accepted and stored."""
    meta = DocstringRaises([], None, None)

    # Empty args list should be stored as is
    assert meta.args == []

    # None description should be stored
    assert meta.description is None

    # None type_name should be stored
    assert meta.type_name is None

def test_docstringraises_description_overwrite():
    """Ensure that the description passed to the subclass is the one stored."""
    # Pass a description to the base class via super, then override in subclass
    base_description = "Base description"
    subclass_description = "Subclass description"
    meta = DocstringRaises(["arg"], subclass_description, "TypeError")

    # The subclass description should override the base description
    assert meta.description == subclass_description
    # The base class's description attribute is the same as the subclass's
    assert isinstance(meta, DocstringMeta)
    assert meta.description == subclass_description

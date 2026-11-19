import pytest
from docstring_parser.common import DocstringRaises, DocstringMeta

def test_docstringraises_initialization(tmp_path):
    """Verify that DocstringRaises stores args, description, and type_name correctly."""
    args = ["ValueError", "TypeError"]
    description = "Raises when input is invalid."
    type_name = "ValueError"
    raises = DocstringRaises(args, description, type_name)

    # Check that the instance is a subclass of DocstringMeta
    assert isinstance(raises, DocstringMeta)

    # Verify that the attributes are set as expected
    assert raises.args == args
    assert raises.description == description
    assert raises.type_name == type_name

def test_docstringraises_with_none_description_and_type(tmp_path):
    """Ensure that None values for description and type_name are handled gracefully."""
    args = ["RuntimeError"]
    raises = DocstringRaises(args, None, None)

    # The description and type_name should be None
    assert raises.description is None
    assert raises.type_name is None
    # args should still be stored correctly
    assert raises.args == args

def test_docstringraises_attribute_mutation(tmp_path):
    """Test that attributes can be mutated after initialization."""
    raises = DocstringRaises([], "Initial", "InitialType")
    # Mutate description and type_name
    raises.description = "Updated description"
    raises.type_name = "UpdatedType"
    # Mutate args list
    raises.args.append("NewError")

    assert raises.description == "Updated description"
    assert raises.type_name == "UpdatedType"
    assert raises.args == ["NewError"]

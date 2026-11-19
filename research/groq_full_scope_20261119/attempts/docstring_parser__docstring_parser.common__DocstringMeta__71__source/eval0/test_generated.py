import pytest
from docstring_parser.common import DocstringMeta


def test_docstring_meta_initialization_with_valid_data():
    """DocstringMeta should store args and description correctly."""
    args = ["arg1", "arg2"]
    description = "This is a test description."
    meta = DocstringMeta(args, description)

    # Assert that the attributes are exactly the values passed
    assert meta.args == args
    assert meta.description == description
    # Ensure that the args list is a separate object (no aliasing)
    assert meta.args is not args
    # Mutating the original list should not affect the stored list
    args.append("arg3")
    assert meta.args == ["arg1", "arg2"]


def test_docstring_meta_with_empty_and_none_values():
    """DocstringMeta should handle empty args list and None description."""
    meta = DocstringMeta([], None)

    # Empty args list should be stored as an empty list
    assert meta.args == []
    # Description can be None
    assert meta.description is None
    # The args attribute should be a list type
    assert isinstance(meta.args, list)


def test_docstring_meta_type_consistency_and_error_behavior():
    """DocstringMeta should raise TypeError when args is not a list."""
    with pytest.raises(TypeError):
        # Passing a tuple should raise a TypeError because the constructor expects a list
        DocstringMeta(("arg1", "arg2"), "desc")

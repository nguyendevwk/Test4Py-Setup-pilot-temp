import pytest
from docstring_parser.common import DocstringMeta


def test_docstring_meta_basic_initialization():
    """Verify that DocstringMeta stores provided arguments and description."""
    args = ["arg1", "arg2"]
    description = "This is a test description."
    meta = DocstringMeta(args, description)

    assert meta.args == args
    assert meta.description == description
    # Ensure that the stored list is the same object (no copy performed)
    assert meta.args is args


def test_docstring_meta_with_empty_and_none():
    """Test boundary conditions: empty args list and None description."""
    meta = DocstringMeta([], None)

    assert meta.args == []
    assert meta.description is None
    # The empty list should be the same instance
    assert meta.args is []


def test_docstring_meta_type_consistency():
    """Ensure that the attributes retain the types passed in."""
    args = ["single"]
    description = "Single description"
    meta = DocstringMeta(args, description)

    assert isinstance(meta.args, list)
    assert isinstance(meta.description, str)
    # Changing the original list after initialization should not affect the stored list
    args.append("new")
    assert meta.args == ["single"]

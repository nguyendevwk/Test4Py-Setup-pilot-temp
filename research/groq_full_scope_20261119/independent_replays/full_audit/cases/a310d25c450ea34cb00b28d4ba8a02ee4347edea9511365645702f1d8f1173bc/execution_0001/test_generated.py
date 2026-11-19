import pytest
from docstring_parser.common import DocstringMeta

def test_normal_initialization():
    """Test that a normal DocstringMeta instance stores the provided args and description."""
    args = ["arg1", "arg2"]
    description = "This is a test description."
    meta = DocstringMeta(args, description)
    assert meta.args == args
    assert meta.description == description

def test_boundary_empty_and_none():
    """Test boundary conditions: empty args list and None description."""
    meta = DocstringMeta([], None)
    assert meta.args == []
    assert meta.description is None

def test_mutability_of_args_list():
    """Test that the args list is stored by reference, so external modifications affect the instance."""
    original = ["initial"]
    meta = DocstringMeta(original, "desc")
    original.append("modified")
    assert meta.args == ["initial", "modified"]

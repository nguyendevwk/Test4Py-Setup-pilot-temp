import pytest
from docstring_parser.common import DocstringMeta


def test_docstring_meta_basic_assignment():
    """Verify that args and description are stored correctly."""
    args = ["param1", "param2"]
    description = "This is a test description."
    meta = DocstringMeta(args, description)
    assert meta.args == args
    assert meta.description == description


def test_docstring_meta_boundary_empty_and_none():
    """Test boundary conditions: empty args list and None description."""
    meta = DocstringMeta([], None)
    assert meta.args == []
    assert meta.description is None


def test_docstring_meta_invalid_args_type():
    """Passing a non-list to args should raise a TypeError when accessed as a list."""
    with pytest.raises(TypeError):
        # The constructor accepts any iterable, but accessing as a list
        # should fail if a non-iterable is passed.
        meta = DocstringMeta("not a list", "desc")
        # Attempt to iterate over args to trigger the error
        _ = [item for item in meta.args]

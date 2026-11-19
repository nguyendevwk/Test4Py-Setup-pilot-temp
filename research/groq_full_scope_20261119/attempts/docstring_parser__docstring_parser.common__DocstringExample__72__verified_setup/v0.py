import pytest
from docstring_parser.common import DocstringExample


def test_docstring_example_normal():
    """Test normal construction with typical values."""
    args = ["param1", "param2"]
    snippet = ">>> example()"
    description = "An example description."
    example = DocstringExample(args, snippet, description)

    # Verify that the attributes are stored correctly
    assert example.args == args
    assert example.snippet == snippet
    assert example.description == description

    # The parent class should have stored the description as well
    assert getattr(example, "description", None) == description


def test_docstring_example_boundary():
    """Test construction with empty and None values."""
    args = []
    snippet = None
    description = None
    example = DocstringExample(args, snippet, description)

    # Empty args list should be preserved
    assert example.args == []

    # None values should be stored as None
    assert example.snippet is None
    assert example.description is None


def test_docstring_example_invalid_args():
    """Test that passing a non-iterable for args raises a TypeError."""
    with pytest.raises(TypeError):
        # Passing None as args should cause the parent constructor to fail
        DocstringExample(None, "snippet", "description")

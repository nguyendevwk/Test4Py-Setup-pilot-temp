import pytest
from docstring_parser.common import DocstringExample, DocstringMeta

def test_docstring_example_initialization_basic():
    """Verify that a DocstringExample correctly stores args, snippet, and description."""
    args = ["param1", "param2"]
    snippet = ">>> example()"
    description = "This is an example."
    example = DocstringExample(args, snippet, description)

    # The base class should store args and description
    assert isinstance(example, DocstringMeta)
    assert example.args == args
    assert example.description == description

    # The subclass should store snippet
    assert example.snippet == snippet

def test_docstring_example_handles_none_values():
    """Ensure that None values for snippet and description are accepted."""
    args = ["only_arg"]
    example = DocstringExample(args, None, None)

    assert example.args == args
    assert example.snippet is None
    assert example.description is None

def test_docstring_example_with_empty_args_and_description():
    """Test behavior when args list is empty and description is an empty string."""
    args = []
    snippet = "print('test')"
    description = ""
    example = DocstringExample(args, snippet, description)

    assert example.args == args
    assert example.snippet == snippet
    assert example.description == description

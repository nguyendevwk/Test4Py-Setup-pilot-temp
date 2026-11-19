import pytest
from docstring_parser.common import DocstringExample, DocstringMeta

def test_docstring_example_initialization_with_all_fields():
    """Verify that all attributes are set correctly when all arguments are provided."""
    args = ["param1", "param2"]
    snippet = ">>> print('hello')"
    description = "Example usage of the function."
    example = DocstringExample(args, snippet, description)

    # Assert that the instance is a subclass of DocstringMeta
    assert isinstance(example, DocstringMeta)

    # Check that the attributes are stored exactly as passed
    assert example.args == args
    assert example.snippet == snippet
    assert example.description == description

def test_docstring_example_initialization_without_snippet():
    """Verify that snippet can be None and is stored correctly."""
    args = ["x"]
    snippet = None
    description = "No snippet provided."
    example = DocstringExample(args, snippet, description)

    assert example.args == args
    assert example.snippet is None
    assert example.description == description

def test_docstring_example_initialization_with_empty_args():
    """Verify that an empty args list is accepted and stored."""
    args = []
    snippet = ">>> foo()"
    description = "Example with no arguments."
    example = DocstringExample(args, snippet, description)

    assert example.args == args
    assert example.snippet == snippet
    assert example.description == description

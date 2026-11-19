import pytest
from docstring_parser.common import DocstringExample

def test_docstring_example_basic_attributes():
    """Verify that a DocstringExample stores args, snippet, and description correctly."""
    args = ["param1", "param2"]
    snippet = ">>> example()"
    description = "This is an example."
    example = DocstringExample(args, snippet, description)

    # The base class should store args and description
    assert example.args == args
    assert example.description == description

    # The subclass should store snippet
    assert example.snippet == snippet

def test_docstring_example_with_none_snippet_and_description():
    """Verify that None values for snippet and description are accepted."""
    args = ["x"]
    example = DocstringExample(args, None, None)

    assert example.args == args
    assert example.snippet is None
    assert example.description is None

def test_docstring_example_immutable_after_initialization():
    """Ensure that the attributes are read‑only after construction."""
    args = ["a", "b"]
    snippet = "print('test')"
    description = "Test description"
    example = DocstringExample(args, snippet, description)

    with pytest.raises(AttributeError):
        example.args = ["new"]
    with pytest.raises(AttributeError):
        example.snippet = "new snippet"
    with pytest.raises(AttributeError):
        example.description = "new description"

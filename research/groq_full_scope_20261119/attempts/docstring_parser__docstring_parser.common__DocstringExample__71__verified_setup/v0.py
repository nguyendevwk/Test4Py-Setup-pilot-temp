import pytest
from docstring_parser.common import DocstringExample, DocstringMeta

def test_normal_initialization(tmp_path):
    """Verify that a normal DocstringExample instance stores all attributes correctly."""
    args = ["param1", "param2"]
    snippet = ">>> example()"
    description = "This is an example."
    example = DocstringExample(args, snippet, description)

    # Assert that the instance is a subclass of DocstringMeta
    assert isinstance(example, DocstringMeta)

    # Check that the attributes are stored as provided
    assert example.args == args
    assert example.snippet == snippet
    assert example.description == description

def test_boundary_none_values(tmp_path):
    """Verify that passing None for optional fields is handled gracefully."""
    args = ["only_arg"]
    example = DocstringExample(args, None, None)

    # Optional fields should be None
    assert example.snippet is None
    assert example.description is None

    # The required args list should still be present
    assert example.args == args

def test_invalid_args_type_raises(tmp_path):
    """Passing a non-list to the args parameter should raise a TypeError."""
    with pytest.raises(TypeError):
        # DocstringMeta.__init__ expects a list; passing None should trigger a TypeError
        DocstringExample(None, "snippet", "description")

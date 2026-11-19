import inspect
import pytest
from docstring_parser.numpydoc import ExamplesSection, DocstringExample

def test_parse_single_example_with_description():
    """Normal case: one snippet followed by a description."""
    section = ExamplesSection(title="Examples", key="examples")
    raw = """\
        >>> import numpy as np
        >>> np.arange(3)
        array([0, 1, 2])
        This returns an array of integers."""
    # cleandoc removes common indentation
    cleaned = inspect.cleandoc(raw)
    parsed = list(section.parse(cleaned))
    assert len(parsed) == 1
    example = parsed[0]
    assert isinstance(example, DocstringExample)
    assert example.args == ["examples"]
    expected_snippet = """\
>>> import numpy as np
>>> np.arange(3)
array([0, 1, 2])"""
    assert example.snippet == expected_snippet
    assert example.description == "This returns an array of integers."

def test_parse_multiple_examples_and_descriptions():
    """Boundary case: multiple snippets separated by descriptions."""
    section = ExamplesSection(title="Examples", key="examples")
    raw = """\
        >>> print('first')
        first
        First example description.
        >>> print('second')
        second
        Second example description."""
    cleaned = inspect.cleandoc(raw)
    parsed = list(section.parse(cleaned))
    assert len(parsed) == 2
    first, second = parsed
    assert first.snippet == ">>> print('first')\n>>> print('first')\nfirst"
    assert first.description == "First example description."
    assert second.snippet == ">>> print('second')\n>>> print('second')\nsecond"
    assert second.description == "Second example description."

def test_parse_no_snippet_returns_none_and_empty_description():
    """Error case: no snippet lines; snippet should be None and description empty."""
    section = ExamplesSection(title="Examples", key="examples")
    raw = """\
        This section contains no code examples."""
    cleaned = inspect.cleandoc(raw)
    parsed = list(section.parse(cleaned))
    assert len(parsed) == 1
    example = parsed[0]
    assert example.snippet is None
    assert example.description == "This section contains no code examples."

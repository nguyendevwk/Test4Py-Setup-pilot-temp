import inspect
import pytest
from docstring_parser.numpydoc import ExamplesSection
from docstring_parser.numpydoc.common import DocstringExample

def test_parse_single_example_with_description():
    section = ExamplesSection(title="Examples", key="examples")
    raw = """
        >>> import numpy as np
        >>> np.array([1, 2, 3])
        array([1, 2, 3])
        This example shows a simple array creation.
    """
    parsed = list(section.parse(raw))
    assert len(parsed) == 1
    example = parsed[0]
    assert isinstance(example, DocstringExample)
    assert example.snippet == (
        ">>> import numpy as np\n"
        ">>> np.array([1, 2, 3])\n"
        "array([1, 2, 3])"
    )
    assert example.description == "This example shows a simple array creation."

def test_parse_multiple_examples_and_empty_description():
    section = ExamplesSection(title="Examples", key="examples")
    raw = """
        >>> print('Hello')
        Hello
        >>> print('World')
        World
        Another example without description.
    """
    parsed = list(section.parse(raw))
    assert len(parsed) == 2
    first, second = parsed
    assert first.snippet == ">>> print('Hello')\nHello"
    assert first.description == ""
    assert second.snippet == ">>> print('World')\nWorld"
    assert second.description == "Another example without description."

def test_parse_no_examples_returns_empty_iterable():
    section = ExamplesSection(title="Examples", key="examples")
    raw = """
        This section contains no code examples.
        Just a plain description.
    """
    parsed = list(section.parse(raw))
    assert parsed == []

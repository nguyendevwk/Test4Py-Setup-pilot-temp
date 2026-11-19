import inspect
import textwrap
import pytest
from docstring_parser.numpydoc import ExamplesSection
from docstring_parser.numpydoc.common import DocstringExample

def test_parse_single_example_with_description():
    raw = textwrap.dedent(
        """\
        >>> import numpy as np
        >>> np.array([1, 2, 3])
        array([1, 2, 3])
        This example shows a simple array creation."""
    )
    section = ExamplesSection()
    result = list(section.parse(inspect.cleandoc(raw)))
    assert len(result) == 1
    example = result[0]
    assert isinstance(example, DocstringExample)
    assert example.snippet == textwrap.dedent(
        """\
        >>> import numpy as np
        >>> np.array([1, 2, 3])"""
    )
    assert example.description == "array([1, 2, 3])\nThis example shows a simple array creation."

def test_parse_multiple_examples():
    raw = textwrap.dedent(
        """\
        >>> a = 1
        >>> a
        1
        First example.
        >>> b = 2
        >>> b
        2
        Second example."""
    )
    section = ExamplesSection()
    result = list(section.parse(inspect.cleandoc(raw)))
    assert len(result) == 2
    first, second = result
    assert first.snippet == ">>> a = 1\n>>> a"
    assert first.description == "1\nFirst example."
    assert second.snippet == ">>> b = 2\n>>> b"
    assert second.description == "2\nSecond example."

def test_parse_no_snippet_returns_description_only():
    raw = textwrap.dedent(
        """\
        This is a description without any code snippet."""
    )
    section = ExamplesSection()
    result = list(section.parse(inspect.cleandoc(raw)))
    assert len(result) == 1
    example = result[0]
    assert example.snippet is None
    assert example.description == "This is a description without any code snippet."

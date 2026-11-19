import pytest
from docstring_parser.numpydoc import ExamplesSection
from docstring_parser.numpydoc.common import DocstringExample

def test_parse_single_example_with_description():
    section = ExamplesSection()
    raw = """\
        >>> import numpy as np
        >>> np.arange(3)
        array([0, 1, 2])
        This example shows a simple array creation."""
    # dedent and strip as parse expects cleaned text
    cleaned = "\n".join([line.strip() for line in raw.splitlines() if line.strip()])
    examples = list(section.parse(cleaned))
    assert len(examples) == 1
    ex = examples[0]
    assert isinstance(ex, DocstringExample)
    assert ex.snippet == ">>> import numpy as np\n>>> np.arange(3)\narray([0, 1, 2])"
    assert ex.description == "This example shows a simple array creation."

def test_parse_multiple_examples_and_empty_description():
    section = ExamplesSection()
    raw = """\
        >>> print('Hello')
        Hello
        >>> print('World')
        World"""
    cleaned = "\n".join([line.strip() for line in raw.splitlines() if line.strip()])
    examples = list(section.parse(cleaned))
    assert len(examples) == 2
    first, second = examples
    assert first.snippet == ">>> print('Hello')\nHello"
    assert first.description == ""
    assert second.snippet == ">>> print('World')\nWorld"
    assert second.description == ""

def test_parse_no_examples_returns_empty_iterable():
    section = ExamplesSection()
    raw = """\
        This section contains no code examples, just text."""
    cleaned = "\n".join([line.strip() for line in raw.splitlines() if line.strip()])
    examples = list(section.parse(cleaned))
    assert examples == []

import inspect
import pytest
from docstring_parser.numpydoc import ExamplesSection, DocstringExample

def test_parse_with_snippet_and_description():
    section = ExamplesSection(title="Examples", key="examples")
    raw = """\
        >>> import numpy as np
        >>> np.arange(3)
        array([0, 1, 2])
        This is a simple example.
        It demonstrates array creation."""
    # cleandoc removes common indentation
    cleaned = inspect.cleandoc(raw)
    result = list(section.parse(cleaned))
    assert len(result) == 1
    example = result[0]
    assert isinstance(example, DocstringExample)
    assert example.args == ["examples"]
    expected_snippet = """\
>>> import numpy as np
>>> np.arange(3)
array([0, 1, 2])"""
    assert example.snippet == expected_snippet
    expected_description = """\
This is a simple example.
It demonstrates array creation."""
    assert example.description == expected_description

def test_parse_with_only_snippet():
    section = ExamplesSection(title="Examples", key="examples")
    raw = """\
        >>> print('Hello')
        Hello"""
    cleaned = inspect.cleandoc(raw)
    result = list(section.parse(cleaned))
    assert len(result) == 1
    example = result[0]
    assert example.snippet == """\
>>> print('Hello')
Hello"""
    assert example.description == ""

def test_parse_with_no_snippet_and_no_description():
    section = ExamplesSection(title="Examples", key="examples")
    raw = ""
    cleaned = inspect.cleandoc(raw)
    result = list(section.parse(cleaned))
    assert result == []

import pytest
from docstring_parser.numpydoc import ExamplesSection
from docstring_parser.numpydoc.common import DocstringExample


def test_parse_normal_example_with_description():
    """Normal case: snippet followed by description."""
    section = ExamplesSection(title="Examples", key="examples")
    text = """
        >>> import numpy as np
        >>> np.arange(3)
        array([0, 1, 2])
        This example shows how to create an array.
    """
    result = list(section.parse(text))
    assert len(result) == 1
    example = result[0]
    assert isinstance(example, DocstringExample)
    assert example.snippet == (
        ">>> import numpy as np\n"
        ">>> np.arange(3)\n"
        "array([0, 1, 2])"
    )
    assert example.description == "This example shows how to create an array."
    assert example.meta == ["examples"]


def test_parse_example_without_description():
    """Boundary case: snippet with no following description."""
    section = ExamplesSection(title="Examples", key="examples")
    text = """
        >>> print('hello')
        hello
    """
    result = list(section.parse(text))
    assert len(result) == 1
    example = result[0]
    assert example.snippet == ">>> print('hello')\nhello"
    assert example.description == ""  # no description lines
    assert example.meta == ["examples"]


def test_parse_empty_section():
    """Error/edge case: empty text yields no examples."""
    section = ExamplesSection(title="Examples", key="examples")
    text = ""
    result = list(section.parse(text))
    assert result == []  # no DocstringExample objects produced

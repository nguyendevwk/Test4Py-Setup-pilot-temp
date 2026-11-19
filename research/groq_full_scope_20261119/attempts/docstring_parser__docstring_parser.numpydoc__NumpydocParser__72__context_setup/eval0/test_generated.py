import inspect
import textwrap
import pytest
from docstring_parser.numpydoc import NumpydocParser, DocstringStyle, DocstringDeprecated, DocstringExample, DocstringParam, DocstringRaises, DocstringReturns

def test_parse_basic_description_and_parameters():
    doc = """
    Short description.

    Long description that spans
    multiple lines.

    Parameters
    ----------
    x : int
        The first parameter.
    y : str, optional
        The second parameter, default is 'foo'.
    """
    parser = NumpydocParser()
    parsed = parser.parse(doc)
    assert parsed.style == DocstringStyle.NUMPYDOC
    assert parsed.short_description == "Short description."
    assert parsed.long_description == "Long description that spans\nmultiple lines."
    assert parsed.blank_after_short_description is True
    assert parsed.blank_after_long_description is False
    params = [m for m in parsed.meta if isinstance(m, DocstringParam)]
    assert len(params) == 2
    x_param = next(p for p in params if p.arg_name == "x")
    assert x_param.type_name == "int"
    assert x_param.is_optional is False
    assert x_param.default is None
    y_param = next(p for p in params if p.arg_name == "y")
    assert y_param.type_name == "str"
    assert y_param.is_optional is True
    assert y_param.default == "foo"

def test_parse_examples_and_deprecation():
    doc = """
    Example usage.

    Examples
    --------
    >>> import math
    >>> math.sqrt(4)
    2.0
    This should return 2.0.

    Deprecated
    ----------
    1.2
    This function is deprecated.
    """
    parser = NumpydocParser()
    parsed = parser.parse(doc)
    examples = [m for m in parsed.meta if isinstance(m, DocstringExample)]
    assert len(examples) == 1
    example = examples[0]
    assert example.snippet == ">>> import math\n>>> math.sqrt(4)"
    assert example.description == "This should return 2.0."
    deprecations = [m for m in parsed.meta if isinstance(m, DocstringDeprecated)]
    assert len(deprecations) == 1
    dep = deprecations[0]
    assert dep.version == "1.2"
    assert dep.description == "This function is deprecated."

def test_parse_empty_and_missing_sections():
    parser = NumpydocParser()
    # Empty docstring should yield only style
    empty = parser.parse("")
    assert empty.style == DocstringStyle.NUMPYDOC
    assert empty.short_description is None
    assert empty.long_description is None
    assert empty.meta == []

    # Docstring with unknown section should be ignored gracefully
    doc = """
    Short.

    Unknown
    ------
    Some text.
    """
    parsed = parser.parse(doc)
    assert parsed.short_description == "Short."
    # No meta entries because section not recognized
    assert parsed.meta == []

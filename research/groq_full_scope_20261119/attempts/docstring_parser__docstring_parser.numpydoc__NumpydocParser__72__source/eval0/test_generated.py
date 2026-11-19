import pytest
from docstring_parser.numpydoc import NumpydocParser
from docstring_parser.common import DocstringStyle, DocstringParam

def test_parse_basic_description_and_params():
    parser = NumpydocParser()
    doc = """
    Short description.

    Long description that spans
    multiple lines.

    Parameters
    ----------
    x : int
        The first parameter.
    y : str
        The second parameter.
    """
    result = parser.parse(doc)
    assert result.style == DocstringStyle.NUMPYDOC
    assert result.short_description == "Short description."
    assert result.long_description == "Long description that spans\nmultiple lines."
    assert result.blank_after_short_description is True
    assert result.blank_after_long_description is False
    assert len(result.meta) == 2
    params = [m for m in result.meta if isinstance(m, DocstringParam)]
    assert len(params) == 2
    assert params[0].name == "x"
    assert params[0].type_name == "int"
    assert params[0].description == "The first parameter."
    assert params[1].name == "y"
    assert params[1].type_name == "str"
    assert params[1].description == "The second parameter."

def test_parse_empty_and_none_input():
    parser = NumpydocParser()
    # Empty string should yield a Docstring with no content
    empty = parser.parse("")
    assert empty.short_description is None
    assert empty.long_description is None
    assert empty.meta == []

    # None input should behave the same as empty string
    none_doc = parser.parse(None)
    assert none_doc.short_description is None
    assert none_doc.long_description is None
    assert none_doc.meta == []

def test_blank_line_handling_in_long_description():
    parser = NumpydocParser()
    doc = """
    Short line.

    \n\nLong description starts after two blank lines.

    Parameters
    ----------
    z : float
        Value.
    """
    result = parser.parse(doc)
    # The long description should start after the two blank lines
    assert result.long_description == "Long description starts after two blank lines."
    # blank_after_short_description should be True because there is a blank line after short description
    assert result.blank_after_short_description is True
    # blank_after_long_description should be False because long description does not end with two newlines
    assert result.blank_after_long_description is False

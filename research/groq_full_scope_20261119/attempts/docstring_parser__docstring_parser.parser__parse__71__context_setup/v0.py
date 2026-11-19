import pytest
from docstring_parser.parser import parse, DocstringStyle, ParseError
from docstring_parser.common import Docstring

def test_parse_google_style_docstring():
    """Verify that a Google style docstring is parsed correctly."""
    doc = """
    Short summary.

    Args:
        x (int): The first number.
        y (int): The second number.

    Returns:
        int: The sum of x and y.
    """
    result = parse(doc, style=DocstringStyle.GOOGLE)
    assert isinstance(result, Docstring)
    assert result.short_description == "Short summary."
    assert len(result.params) == 2
    assert result.params[0].arg_name == "x"
    assert result.params[0].type_name == "int"
    assert result.params[0].description == "The first number."
    assert result.returns[0].type_name == "int"
    assert result.returns[0].description == "The sum of x and y."

def test_parse_empty_string_returns_docstring():
    """Parsing an empty string should return an empty Docstring object."""
    result = parse("", style=DocstringStyle.AUTO)
    assert isinstance(result, Docstring)
    assert result.short_description == ""
    assert result.long_description == ""
    assert result.params == []
    assert result.returns == []

def test_parse_unparsable_raises_parse_error():
    """A string that cannot be parsed by any style should raise ParseError."""
    bad_doc = "<<< not a docstring >>>"
    with pytest.raises(ParseError):
        parse(bad_doc, style=DocstringStyle.AUTO)

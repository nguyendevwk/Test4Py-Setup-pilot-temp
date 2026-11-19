import pytest
from docstring_parser.parser import parse
from docstring_parser.common import DocstringStyle, ParseError, Docstring

def test_parse_google_style_docstring():
    """Verify that a Google‑style docstring is parsed correctly."""
    doc = """
    This function does something.

    Args:
        x (int): The first number.
        y (int): The second number.

    Returns:
        int: The sum of x and y.
    """
    result = parse(doc, style=DocstringStyle.GOOGLE)
    assert isinstance(result, Docstring)
    assert result.short_description == "This function does something."
    assert len(result.params) == 2
    assert result.params[0].arg_name == "x"
    assert result.params[0].type_name == "int"
    assert result.params[0].description == "The first number."
    assert result.returns[0].type_name == "int"
    assert result.returns[0].description == "The sum of x and y."

def test_parse_auto_style_prefers_longest_meta():
    """When style is AUTO, the parser should return the result with the most metadata."""
    doc = """
    Short description.

    Parameters
    ----------
    a : int
        First parameter.
    """
    # The Google parser will produce a Docstring with a param,
    # the NumPy parser will produce a Docstring with a param and a short description,
    # so the NumPy parser should win.
    result = parse(doc, style=DocstringStyle.AUTO)
    assert isinstance(result, Docstring)
    assert len(result.params) == 1
    assert result.short_description == "Short description."

def test_parse_invalid_style_raises():
    """Providing an unsupported style should raise ParseError."""
    with pytest.raises(ParseError):
        parse("Just a string", style=DocstringStyle("INVALID"))

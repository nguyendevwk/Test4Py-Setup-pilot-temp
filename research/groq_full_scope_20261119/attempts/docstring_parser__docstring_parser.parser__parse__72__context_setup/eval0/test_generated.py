import pytest
from docstring_parser.parser import parse, DocstringStyle, ParseError
from docstring_parser.common import Docstring


def test_parse_google_style_returns_docstring():
    """Parsing a Google‑style docstring should return a Docstring instance."""
    google_doc = """
    Short description.

    Args:
        x (int): The first number.
        y (int): The second number.

    Returns:
        int: The sum of x and y.
    """
    result = parse(google_doc, style=DocstringStyle.GOOGLE)
    assert isinstance(result, Docstring)
    assert result.short_description == "Short description."
    assert len(result.params) == 2
    assert result.params[0].arg_name == "x"
    assert result.params[0].type_name == "int"
    assert result.params[0].description == "The first number."
    assert result.returns[0].type_name == "int"
    assert result.returns[0].description == "The sum of x and y."


def test_parse_auto_prefers_style_with_more_meta():
    """AUTO should return the parse result with the most meta information."""
    mixed_doc = """
    Short description.

    Args:
        a (int): First argument.

    Returns:
        int: Result.
    """
    # Explicit Google style parsing
    google_result = parse(mixed_doc, style=DocstringStyle.GOOGLE)
    # AUTO parsing should yield the same result because Google has the most meta
    auto_result = parse(mixed_doc, style=DocstringStyle.AUTO)
    assert google_result == auto_result
    assert len(auto_result.params) == 1
    assert auto_result.params[0].arg_name == "a"


def test_parse_invalid_docstring_raises_parse_error():
    """If no style matches, parse should raise the first ParseError encountered."""
    invalid_doc = "Just some random text that does not conform to any style."
    with pytest.raises(ParseError):
        parse(invalid_doc, style=DocstringStyle.AUTO)

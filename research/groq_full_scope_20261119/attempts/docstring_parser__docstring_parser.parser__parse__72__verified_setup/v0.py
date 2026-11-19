import pytest
from docstring_parser.parser import parse
from docstring_parser.common import DocstringStyle, ParseError, Docstring


def test_parse_google_style_docstring():
    """Verify that a Google style docstring is parsed correctly."""
    docstring = """
    This function does something.

    Args:
        x (int): The first argument.
        y (str): The second argument.

    Returns:
        bool: The result of the operation.
    """
    result: Docstring = parse(docstring, style=DocstringStyle.GOOGLE)

    # The parsed docstring should contain the expected meta information
    assert result.short_description == "This function does something."
    assert len(result.params) == 2
    assert result.params[0].arg_name == "x"
    assert result.params[0].type_name == "int"
    assert result.params[0].description == "The first argument."
    assert result.params[1].arg_name == "y"
    assert result.params[1].type_name == "str"
    assert result.params[1].description == "The second argument."
    assert result.returns is not None
    assert result.returns.type_name == "bool"
    assert result.returns.description == "The result of the operation."


def test_parse_auto_style_prefers_longest_meta():
    """When style is AUTO, the parser should return the style with the most meta."""
    docstring = """
    Short description.

    Parameters
    ----------
    a : int
        First parameter.

    Returns
    -------
    str
        Result string.
    """
    result: Docstring = parse(docstring, style=DocstringStyle.AUTO)

    # The NumPy style parser should be chosen because it provides the most meta
    assert result.meta.get("parameters") is not None
    assert result.meta.get("returns") is not None
    assert result.short_description == "Short description."


def test_parse_none_raises_parse_error():
    """Passing None should raise a ParseError when style is AUTO."""
    with pytest.raises(ParseError):
        parse(None, style=DocstringStyle.AUTO)

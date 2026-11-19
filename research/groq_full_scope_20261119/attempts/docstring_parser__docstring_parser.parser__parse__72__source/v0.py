import pytest
from docstring_parser.parser import parse
from docstring_parser.common import DocstringStyle, ParseError

def test_parse_google_style():
    """Verify that a Google‑style docstring is parsed correctly."""
    doc = """
    This function does something.

    Args:
        x (int): The first argument.
        y (str): The second argument.

    Returns:
        bool: The result.
    """
    result = parse(doc, style=DocstringStyle.GOOGLE)
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
    assert result.returns.description == "The result."

def test_parse_auto_selects_best_style():
    """When style is AUTO, the parser should return the best match."""
    doc = """
    Parameters
    ----------
    a : int
        First parameter.
    b : str
        Second parameter.

    Returns
    -------
    bool
        True if successful.
    """
    result = parse(doc, style=DocstringStyle.AUTO)
    # The NumPy style should be chosen because it matches the structure.
    assert result.short_description == ""
    assert len(result.params) == 2
    assert result.params[0].arg_name == "a"
    assert result.params[0].type_name == "int"
    assert result.params[0].description == "First parameter."
    assert result.returns.type_name == "bool"
    assert result.returns.description == "True if successful."

def test_parse_invalid_text_raises():
    """Parsing text that matches no style should raise ParseError."""
    invalid_doc = "Just a random string that does not conform to any style."
    with pytest.raises(ParseError):
        parse(invalid_doc, style=DocstringStyle.AUTO)

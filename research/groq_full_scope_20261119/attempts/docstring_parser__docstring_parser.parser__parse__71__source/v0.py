import pytest
from docstring_parser.parser import parse
from docstring_parser.common import DocstringStyle, ParseError, Docstring


def test_parse_google_style():
    """Verify that a Google‑style docstring is parsed correctly."""
    google_doc = """
    This function does something.

    Args:
        x (int): The first number.
        y (int): The second number.

    Returns:
        int: The sum of x and y.
    """
    result: Docstring = parse(google_doc, style=DocstringStyle.GOOGLE)

    # Basic structure
    assert result.description.strip() == "This function does something."
    assert len(result.params) == 2
    assert len(result.returns) == 1

    # Parameter details
    param_x = next(p for p in result.params if p.arg_name == "x")
    assert param_x.type_name == "int"
    assert param_x.description.strip() == "The first number."

    param_y = next(p for p in result.params if p.arg_name == "y")
    assert param_y.type_name == "int"
    assert param_y.description.strip() == "The second number."

    # Return details
    ret = result.returns[0]
    assert ret.type_name == "int"
    assert ret.description.strip() == "The sum of x and y."


def test_parse_auto_fallback_to_best_match():
    """When style is AUTO, the parser should return the best match."""
    ambiguous_doc = """
    This function does something.

    Parameters
    ----------
    x : int
        The first number.
    y : int
        The second number.

    Returns
    -------
    int
        The sum of x and y.
    """
    result: Docstring = parse(ambiguous_doc, style=DocstringStyle.AUTO)

    # The NumPy style parser should match best
    assert result.description.strip() == "This function does something."
    assert len(result.params) == 2
    assert len(result.returns) == 1
    assert result.params[0].arg_name == "x"
    assert result.params[1].arg_name == "y"
    assert result.returns[0].type_name == "int"


def test_parse_invalid_style_raises():
    """Parsing with an unsupported style should raise ParseError."""
    bad_doc = "Just a plain string with no docstring structure."
    with pytest.raises(ParseError):
        parse(bad_doc, style=DocstringStyle.REST)  # Assuming REST is unsupported here

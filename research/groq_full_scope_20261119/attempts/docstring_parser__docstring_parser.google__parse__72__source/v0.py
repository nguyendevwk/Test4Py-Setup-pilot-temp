import pytest
from docstring_parser.google import parse
from docstring_parser.common import Docstring, DocstringParam, ParseError

def test_parse_none_returns_empty_docstring():
    """Parsing None should return an empty Docstring instance."""
    result = parse(None)
    assert isinstance(result, Docstring)
    assert result.params == {}
    assert result.returns is None
    assert result.raises == {}
    assert result.examples == {}
    assert result.yields is None
    assert result.meta == {}

def test_parse_simple_google_docstring():
    """A well‑formed Google‑style docstring should be parsed into the correct components."""
    doc = """
    Short description.

    Args:
        x (int): The first number.
        y (str): The second number.

    Returns:
        bool: True if successful.

    Raises:
        ValueError: If the input is invalid.
    """
    result = parse(doc)
    assert isinstance(result, Docstring)
    # Params
    assert "x" in result.params
    assert isinstance(result.params["x"], DocstringParam)
    assert result.params["x"].type_name == "int"
    assert result.params["x"].description == "The first number."
    assert "y" in result.params
    assert result.params["y"].type_name == "str"
    # Returns
    assert result.returns is not None
    assert result.returns.type_name == "bool"
    assert result.returns.description == "True if successful."
    # Raises
    assert "ValueError" in result.raises
    assert result.raises["ValueError"].description == "If the input is invalid."

def test_parse_malformed_docstring_raises_error():
    """A malformed Google‑style docstring should raise ParseError."""
    malformed = """
    Args:
        x int The missing colon.
    """
    with pytest.raises(ParseError):
        parse(malformed)

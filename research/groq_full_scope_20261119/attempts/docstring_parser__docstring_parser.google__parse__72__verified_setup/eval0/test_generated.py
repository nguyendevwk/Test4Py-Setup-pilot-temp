import pytest
from docstring_parser.google import parse
from docstring_parser.common import Docstring, DocstringParam, DocstringReturns, DocstringRaises

def test_parse_empty_docstring():
    """Parsing an empty string should return a Docstring with no components."""
    result = parse("")
    assert isinstance(result, Docstring)
    assert result.short_description == ""
    assert result.long_description == ""
    assert result.params == {}
    assert result.returns is None
    assert result.raises == {}
    assert result.examples == []

def test_parse_full_docstring():
    """A complete Google‑style docstring should be parsed into all expected parts."""
    doc = """
    Short description.

    Long description spanning
    multiple lines.

    Args:
        x (int): The first argument.
        y (str): The second argument.

    Returns:
        bool: True if successful.

    Raises:
        ValueError: If an error occurs.
    """
    result = parse(doc)
    assert isinstance(result, Docstring)
    assert result.short_description == "Short description."
    assert "Long description spanning" in result.long_description
    assert set(result.params.keys()) == {"x", "y"}
    assert isinstance(result.params["x"], DocstringParam)
    assert result.params["x"].type_name == "int"
    assert result.params["x"].description == "The first argument."
    assert isinstance(result.returns, DocstringReturns)
    assert result.returns.type_name == "bool"
    assert result.returns.description == "True if successful."
    assert set(result.raises.keys()) == {"ValueError"}
    assert isinstance(result.raises["ValueError"], DocstringRaises)
    assert result.raises["ValueError"].description == "If an error occurs."

def test_parse_invalid_type_raises():
    """Passing a non‑string type should raise a TypeError."""
    with pytest.raises(TypeError):
        parse(42)  # type: ignore[arg-type]

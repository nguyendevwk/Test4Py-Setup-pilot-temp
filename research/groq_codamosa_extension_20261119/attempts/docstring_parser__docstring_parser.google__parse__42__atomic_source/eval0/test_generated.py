import pytest
from docstring_parser.google import parse
from docstring_parser.common import ParseError, Docstring, DocstringParam, DocstringReturns, DocstringRaises

def test_parse_basic_docstring():
    """Verify that a simple Google‑style docstring is parsed correctly."""
    doc = """
    Short summary.

    Longer description that spans multiple lines.

    Args:
        x (int): The first argument.
        y (str): The second argument.

    Returns:
        bool: True if successful, False otherwise.

    Raises:
        ValueError: If the input is invalid.
    """
    result = parse(doc)

    # Basic structure
    assert isinstance(result, Docstring)
    assert result.short_description == "Short summary."
    assert "Longer description" in result.long_description

    # Parameters
    assert len(result.params) == 2
    param_x = next(p for p in result.params if p.arg_name == "x")
    assert isinstance(param_x, DocstringParam)
    assert param_x.type_name == "int"
    assert param_x.description == "The first argument."

    # Returns
    assert len(result.returns) == 1
    ret = result.returns[0]
    assert isinstance(ret, DocstringReturns)
    assert ret.type_name == "bool"
    assert ret.description == "True if successful, False otherwise."

    # Raises
    assert len(result.raises) == 1
    r = result.raises[0]
    assert isinstance(r, DocstringRaises)
    assert r.type_name == "ValueError"
    assert r.description == "If the input is invalid."

def test_parse_empty_and_none():
    """Empty string or None should yield an empty Docstring without errors."""
    for input_text in ("", None):
        result = parse(input_text)
        assert isinstance(result, Docstring)
        assert result.short_description == ""
        assert result.long_description == ""
        assert result.params == []
        assert result.returns == []
        assert result.raises == []

def test_parse_invalid_section_raises_error():
    """A malformed docstring should raise ParseError."""
    bad_doc = """
    Summary.

    Args:
        x (int) The missing colon after type.
    """
    with pytest.raises(ParseError):
        parse(bad_doc)

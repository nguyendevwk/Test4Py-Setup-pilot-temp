import pytest
from docstring_parser.google import parse
from docstring_parser.common import Docstring, ParseError

def test_parse_simple_google_style():
    """Test parsing of a minimal Google‑style docstring."""
    doc = """\
This function does something.

Args:
    x (int): The first argument.
    y (str): The second argument.

Returns:
    bool: True if successful, False otherwise.
"""
    result = parse(doc)
    assert isinstance(result, Docstring)
    # Check that the description is captured correctly
    assert result.short_description == "This function does something."
    # There should be two parameters
    assert len(result.params) == 2
    param_names = {p.arg_name for p in result.params}
    assert param_names == {"x", "y"}
    # Check return description
    assert result.returns is not None
    assert result.returns.type_name == "bool"
    assert result.returns.description == "True if successful, False otherwise."

def test_parse_boundary_empty_and_none():
    """Test parsing of an empty string and None."""
    # Empty string should produce a Docstring with empty fields
    empty = parse("")
    assert isinstance(empty, Docstring)
    assert empty.short_description == ""
    assert empty.long_description == ""
    assert empty.params == []
    assert empty.returns is None
    # None should be treated the same as empty string
    none_doc = parse(None)
    assert isinstance(none_doc, Docstring)
    assert none_doc.short_description == ""
    assert none_doc.long_description == ""
    assert none_doc.params == []
    assert none_doc.returns is None

def test_parse_invalid_format_raises_error():
    """Test that a malformed Google‑style docstring raises ParseError."""
    bad_doc = """\
This is a bad docstring.

Arguments:
    x (int): missing 'Args:' keyword.
"""
    with pytest.raises(ParseError):
        parse(bad_doc)

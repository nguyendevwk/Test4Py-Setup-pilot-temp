import pytest
from docstring_parser.google import parse
from docstring_parser.common import Docstring, ParseError

def test_parse_basic_google_style():
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
        ValueError: If an error occurs.

    Examples:
        >>> result = func(1, 'a')
        >>> assert result is True
    """
    parsed = parse(doc)
    assert isinstance(parsed, Docstring)
    # Summary and description
    assert parsed.short_description == "Short summary."
    assert parsed.long_description.strip().startswith("Longer description")
    # Parameters
    assert len(parsed.params) == 2
    param_names = {p.arg_name for p in parsed.params}
    assert param_names == {"x", "y"}
    # Return
    assert parsed.returns is not None
    assert parsed.returns.type_name == "bool"
    # Raises
    assert len(parsed.raises) == 1
    assert parsed.raises[0].type_name == "ValueError"
    # Examples
    assert len(parsed.examples) == 1
    assert parsed.examples[0].example_text.strip().startswith(">>> result = func")

def test_parse_empty_and_none():
    """Parsing an empty string or None should yield an empty Docstring."""
    empty = parse("")
    assert isinstance(empty, Docstring)
    assert empty.short_description == ""
    assert empty.long_description == ""
    assert empty.params == []
    assert empty.returns is None
    assert empty.raises == []
    assert empty.examples == []

    none_doc = parse(None)
    assert isinstance(none_doc, Docstring)
    assert none_doc.short_description == ""
    assert none_doc.long_description == ""
    assert none_doc.params == []
    assert none_doc.returns is None
    assert none_doc.raises == []
    assert none_doc.examples == []

def test_parse_invalid_format_raises_error():
    """A malformed Google‑style docstring should raise ParseError."""
    bad_doc = """
    Summary line

    Args
        x (int): missing colon after section header
    """
    with pytest.raises(ParseError):
        parse(bad_doc)

import pytest
from docstring_parser.google import parse
from docstring_parser.common import Docstring, DocstringParam, DocstringReturns, DocstringRaises, DocstringExample

def test_parse_simple_google_style_docstring():
    """Verify that a minimal Google‑style docstring is parsed correctly."""
    docstring_text = """
    Short summary.

    Args:
        x (int): The first argument.
        y (str): The second argument.

    Returns:
        bool: True if successful.

    Raises:
        ValueError: If an error occurs.

    Examples:
        >>> result = my_func(1, 'a')
        >>> assert result is True
    """
    doc = parse(docstring_text)

    # Basic structure
    assert isinstance(doc, Docstring)
    assert doc.short_description == "Short summary."
    assert doc.long_description == ""

    # Parameters
    assert len(doc.params) == 2
    param_names = {p.arg_name for p in doc.params}
    assert param_names == {"x", "y"}
    x_param = next(p for p in doc.params if p.arg_name == "x")
    assert x_param.type_name == "int"
    assert x_param.description == "The first argument."

    # Returns
    assert len(doc.returns) == 1
    ret = doc.returns[0]
    assert isinstance(ret, DocstringReturns)
    assert ret.type_name == "bool"
    assert ret.description == "True if successful."

    # Raises
    assert len(doc.raises) == 1
    raise_item = doc.raises[0]
    assert isinstance(raise_item, DocstringRaises)
    assert raise_item.type_name == "ValueError"
    assert raise_item.description == "If an error occurs."

    # Examples
    assert len(doc.examples) == 1
    example = doc.examples[0]
    assert isinstance(example, DocstringExample)
    assert example.code.strip() == ">>> result = my_func(1, 'a')\n>>> assert result is True"

def test_parse_empty_and_none_input():
    """Parsing an empty string or None should yield an empty Docstring."""
    empty_doc = parse("")
    none_doc = parse(None)

    for doc in (empty_doc, none_doc):
        assert isinstance(doc, Docstring)
        assert doc.short_description == ""
        assert doc.long_description == ""
        assert doc.params == []
        assert doc.returns == []
        assert doc.raises == []
        assert doc.examples == []

def test_parse_invalid_section_raises_error():
    """A malformed section header should raise ParseError."""
    malformed_text = """
    Short summary.

    Parameters:
        x (int): The first argument.
    """
    from docstring_parser.common import ParseError
    with pytest.raises(ParseError):
        parse(malformed_text)

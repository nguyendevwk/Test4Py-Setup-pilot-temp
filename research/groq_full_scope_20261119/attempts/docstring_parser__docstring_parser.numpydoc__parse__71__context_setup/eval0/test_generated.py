import inspect
import pytest
from docstring_parser.numpydoc import parse, DocstringStyle, Docstring

def test_parse_basic_docstring():
    doc = """
    Short description.

    Long description that spans
    multiple lines.

    Parameters
    ----------
    x : int
        The first parameter.
    y : str
        The second parameter.

    Returns
    -------
    bool
        True if successful.
    """
    result = parse(doc)
    assert isinstance(result, Docstring)
    assert result.style == DocstringStyle.NUMPYDOC
    assert result.short_description == "Short description."
    assert result.long_description == "Long description that spans\nmultiple lines."
    assert result.blank_after_short_description is True
    assert result.blank_after_long_description is False
    meta = {m.args[0]: m.description for m in result.meta}
    assert meta["param"] == "x : int\n    The first parameter.\ny : str\n    The second parameter."
    assert meta["returns"] == "bool\n    True if successful."

def test_parse_empty_and_none():
    assert parse("") == Docstring(style=DocstringStyle.NUMPYDOC)
    assert parse(None) == Docstring(style=DocstringStyle.NUMPYDOC)

def test_parse_no_sections_only_description():
    doc = """
    Only short description.

    Only long description.
    """
    result = parse(doc)
    assert result.short_description == "Only short description."
    assert result.long_description == "Only long description."
    assert result.meta == []
    assert result.blank_after_short_description is True
    assert result.blank_after_long_description is False

import pytest
from docstring_parser.numpydoc import parse
from docstring_parser.common import Docstring, DocstringParam, DocstringReturns, DocstringRaises

def test_parse_basic_docstring():
    """Test that a simple numpy‑style docstring is parsed correctly."""
    doc = """
    Short summary.

    Parameters
    ----------
    x : int
        The first parameter.
    y : str, optional
        The second parameter.

    Returns
    -------
    bool
        True if successful.

    Raises
    ------
    ValueError
        If an error occurs.
    """
    parsed = parse(doc)
    assert isinstance(parsed, Docstring)
    # Parameters
    assert len(parsed.params) == 2
    x_param = next(p for p in parsed.params if p.arg_name == "x")
    assert isinstance(x_param, DocstringParam)
    assert x_param.type_name == "int"
    assert x_param.description.strip() == "The first parameter."
    y_param = next(p for p in parsed.params if p.arg_name == "y")
    assert y_param.type_name == "str, optional"
    # Returns
    assert len(parsed.returns) == 1
    ret = parsed.returns[0]
    assert isinstance(ret, DocstringReturns)
    assert ret.type_name == "bool"
    assert ret.description.strip() == "True if successful."
    # Raises
    assert len(parsed.raises) == 1
    raise_item = parsed.raises[0]
    assert isinstance(raise_item, DocstringRaises)
    assert raise_item.type_name == "ValueError"
    assert raise_item.description.strip() == "If an error occurs."

def test_parse_empty_and_none():
    """Test that an empty string or None returns an empty Docstring."""
    empty = parse("")
    none_doc = parse(None)
    for result in (empty, none_doc):
        assert isinstance(result, Docstring)
        assert result.params == []
        assert result.returns == []
        assert result.raises == []
        assert result.short_description == ""
        assert result.long_description == ""

def test_parse_invalid_section_raises():
    """Test that an invalid section header raises a ValueError."""
    bad_doc = """
    Short summary.

    Parameters
    ----------
    x : int
        The first parameter.

    InvalidSection
    --------------
    Something unexpected.
    """
    with pytest.raises(ValueError):
        parse(bad_doc)

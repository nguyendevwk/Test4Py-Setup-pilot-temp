import pytest
from docstring_parser.numpydoc import parse
from docstring_parser.common import Docstring, DocstringParam, DocstringReturns, DocstringRaises

def test_parse_full_docstring():
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
    param_names = {p.arg_name for p in parsed.params}
    assert param_names == {"x", "y"}
    x_param = next(p for p in parsed.params if p.arg_name == "x")
    assert isinstance(x_param, DocstringParam)
    assert x_param.type_name == "int"
    assert x_param.description.strip() == "The first parameter."

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
    # Empty string should produce an empty Docstring
    empty = parse("")
    assert isinstance(empty, Docstring)
    assert empty.params == []
    assert empty.returns == []
    assert empty.raises == []

    # None should also produce an empty Docstring
    none_doc = parse(None)
    assert isinstance(none_doc, Docstring)
    assert none_doc.params == []
    assert none_doc.returns == []
    assert none_doc.raises == []

def test_parse_missing_sections():
    doc = """
    Short summary.

    Parameters
    ----------
    a : float
        A float value.
    """
    parsed = parse(doc)
    assert isinstance(parsed, Docstring)

    # Only params present
    assert len(parsed.params) == 1
    assert parsed.params[0].arg_name == "a"
    assert parsed.params[0].type_name == "float"

    # No returns or raises
    assert parsed.returns == []
    assert parsed.raises == []

import pytest
from docstring_parser.numpydoc import parse
from docstring_parser.common import Docstring, DocstringParam, DocstringReturns, DocstringRaises

def test_parse_full_numpydoc():
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
    assert x_param.type_name == "int"
    assert x_param.description.strip() == "The first parameter."
    y_param = next(p for p in parsed.params if p.arg_name == "y")
    assert y_param.type_name == "str, optional"
    assert y_param.description.strip() == "The second parameter."
    # Returns
    assert len(parsed.returns) == 1
    ret = parsed.returns[0]
    assert isinstance(ret, DocstringReturns)
    assert ret.type_name == "bool"
    assert ret.description.strip() == "True if successful."
    # Raises
    assert len(parsed.raises) == 1
    exc = parsed.raises[0]
    assert isinstance(exc, DocstringRaises)
    assert exc.type_name == "ValueError"
    assert exc.description.strip() == "If an error occurs."

def test_parse_partial_numpydoc():
    doc = """
    Short summary.

    Parameters
    ----------
    a : float
        A value.

    """
    parsed = parse(doc)
    assert isinstance(parsed, Docstring)
    assert len(parsed.params) == 1
    assert parsed.params[0].arg_name == "a"
    assert parsed.params[0].type_name == "float"
    assert parsed.params[0].description.strip() == "A value."
    # No returns or raises
    assert parsed.returns == []
    assert parsed.raises == []

def test_parse_none_returns_empty_docstring():
    parsed = parse(None)
    assert isinstance(parsed, Docstring)
    assert parsed.params == []
    assert parsed.returns == []
    assert parsed.raises == []
    assert parsed.short_description == ""
    assert parsed.long_description == ""

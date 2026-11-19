import pytest
from docstring_parser.numpydoc import parse
from docstring_parser.common import Docstring, DocstringParam, DocstringReturns, DocstringRaises

def test_parse_basic_docstring():
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
    # Summary
    assert parsed.short_description == "Short summary."
    # Parameters
    assert len(parsed.params) == 2
    names = {p.arg_name for p in parsed.params}
    assert names == {"x", "y"}
    # Return
    assert len(parsed.returns) == 1
    ret = parsed.returns[0]
    assert isinstance(ret, DocstringReturns)
    assert ret.type_name == "bool"
    # Raises
    assert len(parsed.raises) == 1
    raise_item = parsed.raises[0]
    assert isinstance(raise_item, DocstringRaises)
    assert raise_item.type_name == "ValueError"

def test_parse_empty_and_none():
    # Empty string should produce an empty Docstring
    empty = parse("")
    assert isinstance(empty, Docstring)
    assert empty.short_description == ""
    assert empty.long_description == ""
    assert empty.params == []
    assert empty.returns == []
    assert empty.raises == []

    # None input should also produce an empty Docstring
    none_doc = parse(None)
    assert isinstance(none_doc, Docstring)
    assert none_doc.short_description == ""
    assert none_doc.long_description == ""
    assert none_doc.params == []
    assert none_doc.returns == []
    assert none_doc.raises == []

def test_parse_with_complex_types_and_defaults():
    doc = """
    Complex docstring.

    Parameters
    ----------
    data : list[dict[str, int]]
        A list of dictionaries.
    flag : bool = True
        Optional flag.

    Returns
    -------
    tuple[int, str]
        A tuple containing an integer and a string.

    Raises
    ------
    RuntimeError
        If something bad happens.
    """
    parsed = parse(doc)
    # Check parameter types and defaults
    param_dict = {p.arg_name: p for p in parsed.params}
    assert param_dict["data"].type_name == "list[dict[str, int]]"
    assert param_dict["flag"].default == "True"
    # Return type
    ret = parsed.returns[0]
    assert ret.type_name == "tuple[int, str]"
    # Raise type
    raise_item = parsed.raises[0]
    assert raise_item.type_name == "RuntimeError"

import pytest
from docstring_parser.numpydoc import parse
from docstring_parser.common import DocstringParam, DocstringReturns


def test_parse_numpydoc_basic():
    text = """Short summary line.

Parameters
----------
param1 : int
    The first parameter.

Returns
-------
bool
    True if successful.
"""
    doc = parse(text)

    # Basic Docstring attributes
    assert doc.short_description == "Short summary line."
    assert doc.blank_after_short_description is True
    assert doc.long_description is None
    assert doc.description.strip() == "Short summary line."

    # Meta items
    assert len(doc.meta) == 2
    param = doc.params[0]
    assert isinstance(param, DocstringParam)
    assert param.arg_name == "param1"
    assert param.type_name == "int"
    assert param.description == "The first parameter."
    assert doc.params_by_name["param1"] is param

    returns_item = next(m for m in doc.meta if isinstance(m, DocstringReturns))
    assert returns_item.type_name == "bool"
    assert returns_item.description == "True if successful."

    # Empty docstring
    empty_doc = parse(None)
    assert empty_doc.description is None
    assert empty_doc.params == []

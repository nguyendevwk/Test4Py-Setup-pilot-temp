import pytest
from docstring_parser.numpydoc import parse


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

    # Short description and blank line handling
    assert doc.short_description == "Short summary line."
    assert doc.blank_after_short_description is True
    assert doc.long_description is None
    assert doc.description == "Short summary line.\n"

    # Parameters parsing
    assert len(doc.params) == 1
    param = doc.params[0]
    assert param.arg_name == "param1"
    assert param.type_name == "int"
    assert param.description == "The first parameter."
    assert doc.params_by_name["param1"] is param

    # Empty docstring
    empty_doc = parse(None)
    assert empty_doc.description is None
    assert empty_doc.params == []

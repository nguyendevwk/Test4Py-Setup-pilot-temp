import pytest
from docstring_parser.numpydoc import parse


def test_parse_numpydoc_basic_and_none():
    # Canonical numpy‑style docstring
    text = '''Short summary line.

Parameters
----------
param1 : int
    The first parameter.

Returns
-------
bool
    True if successful.
'''
    doc = parse(text)

    # Short description and overall description
    assert doc.short_description == "Short summary line."
    assert doc.description == "Short summary line."
    assert doc.long_description is None

    # Parameters section
    assert len(doc.params) == 1
    param = doc.params[0]
    assert param.arg_name == "param1"
    assert param.type_name == "int"
    assert param.description.strip() == "The first parameter."

    # No raises or attrs sections
    assert doc.raises == []
    assert doc.attrs == []

    # Parsing None yields an empty Docstring
    empty_doc = parse(None)
    assert empty_doc.description is None
    assert empty_doc.params == []

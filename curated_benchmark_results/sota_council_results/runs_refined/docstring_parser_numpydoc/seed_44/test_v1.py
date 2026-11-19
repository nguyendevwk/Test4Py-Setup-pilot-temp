import pytest
from docstring_parser.numpydoc import parse
from docstring_parser.common import Docstring


def test_parse_numpydoc_sections():
    docstring = """Summary line.

Extended description continues here.

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

Raises
------
ValueError
    If an error occurs.
"""
    doc = parse(docstring)

    assert isinstance(doc, Docstring)
    assert doc.short_description == "Summary line."
    assert "Extended description continues" in doc.long_description

    assert len(doc.params) == 2
    param_names = {p.arg_name for p in doc.params}
    assert param_names == {"x", "y"}

    assert doc.returns is not None
    assert doc.returns.type_name == "bool"
    assert doc.returns.description == "True if successful."

    assert len(doc.raises) == 1
    raise_item = doc.raises[0]
    assert raise_item.type_name == "ValueError"
    assert raise_item.description == "If an error occurs."

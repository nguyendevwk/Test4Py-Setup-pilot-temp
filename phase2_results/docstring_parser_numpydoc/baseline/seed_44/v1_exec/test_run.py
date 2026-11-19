import pytest
from docstring_parser.numpydoc import parse
from docstring_parser.core import Docstring, Parameter, Return

def test_parse_numpydoc_parses_parameters_and_returns():
    docstring = """\
This is a test function.

Parameters
----------
x : int
    The first parameter.
y : float
    The second parameter.

Returns
-------
int
    The result.
"""
    doc = parse(docstring)
    assert isinstance(doc, Docstring)
    assert doc.summary == "This is a test function."
    assert doc.description == ""
    assert len(doc.parameters) == 2
    assert [p.name for p in doc.parameters] == ["x", "y"]
    assert [p.type_name for p in doc.parameters] == ["int", "float"]
    assert [p.description for p in doc.parameters] == ["The first parameter.", "The second parameter."]
    assert isinstance(doc.returns, Return)
    assert doc.returns.type_name == "int"
    assert doc.returns.description == "The result."
    assert doc.raises == []
    assert doc.examples == []

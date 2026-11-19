import pytest
from docstring_parser.numpydoc import parse
from docstring_parser import Docstring

def test_parse_numpydoc_docstring_parses_expected_components():
    docstring_text = """This is a summary.

This is a description that spans multiple lines.

Parameters
----------
x : int
    The first parameter.
y : str, optional
    The second parameter.

Returns
-------
bool
    True if successful, False otherwise.
"""
    doc = parse(docstring_text)
    assert isinstance(doc, Docstring)
    assert doc.summary == "This is a summary."
    assert "This is a description" in doc.description
    assert len(doc.params) == 2

    param_x = doc.params[0]
    assert param_x.arg_name == "x"
    assert param_x.type_name == "int"
    assert param_x.description.strip() == "The first parameter."
    assert param_x.optional is False

    param_y = doc.params[1]
    assert param_y.arg_name == "y"
    assert param_y.type_name == "str"
    assert param_y.description.strip() == "The second parameter."
    assert param_y.optional is True

    assert doc.returns.type_name == "bool"
    assert doc.returns.description.strip() == "True if successful, False otherwise."

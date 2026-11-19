import pytest
from docstring_parser.rest import parse
from docstring_parser import Docstring

def test_parse_rest_docstring_parses_sections_correctly():
    docstring = """Short description.

Long description line 1.
Long description line 2.

Args:
    x (int): The first argument.
    y (str): The second argument.

Returns:
    bool: True if successful.

Raises:
    ValueError: If something goes wrong.
"""
    doc = parse(docstring)
    assert isinstance(doc, Docstring)
    assert doc.short_description == "Short description."
    assert doc.long_description == "Long description line 1.\nLong description line 2."
    assert len(doc.params) == 2
    x_param, y_param = doc.params
    assert x_param.name == "x"
    assert x_param.type_name == "int"
    assert x_param.description == "The first argument."
    assert y_param.name == "y"
    assert y_param.type_name == "str"
    assert y_param.description == "The second argument."
    assert doc.returns is not None
    assert doc.returns.type_name == "bool"
    assert doc.returns.description == "True if successful."
    assert len(doc.raises) == 1
    raise_obj = doc.raises[0]
    assert raise_obj.type_name == "ValueError"
    assert raise_obj.description == "If something goes wrong."

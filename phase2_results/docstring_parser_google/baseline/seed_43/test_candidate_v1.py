import pytest
from docstring_parser.google import parse

def test_parse_google_style_docstring_parses_sections_correctly():
    docstring = """Short description.

Long description line 1.
Long description line 2.

Args:
    x (int): The first argument.
    y (str): The second argument.

Returns:
    bool: True if successful.

Raises:
    ValueError: If an error occurs.

Examples:
    >>> foo(1, 'a')
    True
"""
    doc = parse(docstring)
    assert doc.short_description == "Short description."
    assert doc.long_description == "Long description line 1.\nLong description line 2."
    assert len(doc.params) == 2
    x_param, y_param = doc.params
    assert (x_param.name, x_param.type_name, x_param.description) == ("x", "int", "The first argument.")
    assert (y_param.name, y_param.type_name, y_param.description) == ("y", "str", "The second argument.")
    assert (doc.returns.type_name, doc.returns.description) == ("bool", "True if successful.")
    assert len(doc.raises) == 1
    raise_obj = doc.raises[0]
    assert (raise_obj.type_name, raise_obj.description) == ("ValueError", "If an error occurs.")
    assert len(doc.examples) == 1
    example = doc.examples[0]
    assert example.code.strip() == ">>> foo(1, 'a')\n    True"

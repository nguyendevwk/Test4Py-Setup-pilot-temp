import pytest
from docstring_parser.rest import parse
from docstring_parser.docstring import Docstring, Parameter, Return, Raise


def test_parse_rest_docstring_sections():
    docstring = """Short description.

Long description line 1.
Long description line 2.

Args:
    x (int): The first argument.
    y (str): The second argument.

Returns:
    bool: True if successful.

Raises:
    ValueError: If input is invalid."""
    doc = parse(docstring)

    assert isinstance(doc, Docstring)
    assert doc.short_description == "Short description."
    assert doc.long_description == "Long description line 1.\nLong description line 2."

    assert len(doc.params) == 2
    p1, p2 = doc.params
    assert isinstance(p1, Parameter)
    assert p1.name == "x"
    assert p1.type == "int"
    assert p1.description == "The first argument."
    assert isinstance(p2, Parameter)
    assert p2.name == "y"
    assert p2.type == "str"
    assert p2.description == "The second argument."

    assert isinstance(doc.returns, Return)
    assert doc.returns.type == "bool"
    assert doc.returns.description == "True if successful."

    assert len(doc.raises) == 1
    r = doc.raises[0]
    assert isinstance(r, Raise)
    assert r.type == "ValueError"
    assert r.description == "If input is invalid."

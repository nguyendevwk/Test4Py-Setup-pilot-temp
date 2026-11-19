import pytest
from docstring_parser.rest import parse
from docstring_parser.docstring import Docstring

def test_parse_rest_docstring_parses_sections_correctly():
    docstring_text = """Short description.

Long description line 1.
Long description line 2.

:param x: description of x
:param y: description of y
:return: result
"""
    doc = parse(docstring_text)
    assert isinstance(doc, Docstring)
    assert doc.short_description == "Short description."
    assert doc.long_description == "Long description line 1.\nLong description line 2."
    assert len(doc.params) == 2
    assert doc.params[0].name == "x"
    assert doc.params[0].description == "description of x"
    assert doc.params[1].name == "y"
    assert doc.params[1].description == "description of y"
    assert doc.returns is not None
    assert doc.returns.description == "result"
    assert len(doc.raises) == 0

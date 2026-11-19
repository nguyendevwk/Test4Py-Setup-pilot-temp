import pytest
from docstring_parser.google import parse
from docstring_parser.common import Docstring

def test_parse_empty_docstring_returns_empty_docstring():
    """`parse` should return a Docstring with no description or sections when given an empty string."""
    doc: Docstring = parse("")
    # The description should be None or an empty string for an empty docstring
    assert doc.description in (None, "")
    # No parameters, returns, or other sections should be present
    assert not getattr(doc, "params", [])
    assert not getattr(doc, "returns", [])
    assert not getattr(doc, "raises", [])
    assert not getattr(doc, "examples", [])
    assert not getattr(doc, "methods", [])
    assert not getattr(doc, "deprecation", [])

import pytest
from docstring_parser.google import parse


def test_parse_none_returns_empty_docstring():
    """`parse(None)` should return a Docstring with no description and no params."""
    doc = parse(None)
    # The returned object should be a Docstring instance
    assert hasattr(doc, "description")
    assert hasattr(doc, "params")
    # No description should be present
    assert doc.description is None
    # No parameters should be parsed
    assert isinstance(doc.params, list)
    assert len(doc.params) == 0

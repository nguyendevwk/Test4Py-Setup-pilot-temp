import pytest
from docstring_parser.google import parse
from docstring_parser.common import Docstring


def test_parse_empty_docstring_returns_empty_docstring():
    """`parse` should return a Docstring with empty description and no sections for an empty string."""
    result = parse("")
    assert isinstance(result, Docstring)
    assert result.description == ""
    assert result.sections == []

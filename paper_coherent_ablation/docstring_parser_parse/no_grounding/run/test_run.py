import pytest
from docstring_parser.parser import parse
from docstring_parser.common import BaseParser

def test_parse_raises_value_error_when_sections_provided_with_parser():
    """`parse` should raise ValueError if a BaseParser instance is supplied with non‑None sections."""
    with pytest.raises(ValueError):
        parse("sample docstring", style=BaseParser(), sections=[1])

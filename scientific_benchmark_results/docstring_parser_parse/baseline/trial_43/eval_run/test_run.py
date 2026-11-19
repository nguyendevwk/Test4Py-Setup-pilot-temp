import pytest
from docstring_parser.parser import parse, BaseParser


def test_parse_raises_value_error_when_sections_provided_with_base_parser():
    """`parse` should raise ValueError if a BaseParser is used with non‑None sections."""
    with pytest.raises(ValueError):
        parse("dummy text", style=BaseParser(), sections=[1])

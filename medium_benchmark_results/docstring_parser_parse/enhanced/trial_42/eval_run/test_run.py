import pytest
from docstring_parser.parser import parse
from docstring_parser.common import BaseParser

def test_parse_with_baseparser_and_sections_raises_value_error():
    """parse should raise ValueError when a BaseParser is given with non‑None sections."""
    with pytest.raises(ValueError):
        parse("sample text", style=BaseParser(), sections=[])

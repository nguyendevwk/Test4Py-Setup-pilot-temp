import pytest
from docstring_parser.parser import parse
from docstring_parser.common import BaseParser

def test_parse_raises_value_error_when_sections_provided_with_baseparser():
    """parse should raise ValueError if a BaseParser is given with non‑None sections."""
    with pytest.raises(ValueError):
        parse("doc", style=BaseParser(), sections=[1])

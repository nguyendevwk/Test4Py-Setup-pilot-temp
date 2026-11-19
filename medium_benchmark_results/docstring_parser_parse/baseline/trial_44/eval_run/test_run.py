import pytest
from docstring_parser.parser import parse
from docstring_parser import google

def test_parse_with_parser_and_sections_raises():
    """parse should raise ValueError when a parser is supplied with non‑None sections."""
    with pytest.raises(ValueError, match="A parser has its sections; pass none"):
        parse("sample text", style=google, sections=[None])

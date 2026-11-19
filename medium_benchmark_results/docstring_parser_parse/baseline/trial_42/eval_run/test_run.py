import pytest
from docstring_parser.parser import parse
from docstring_parser.common import BaseParser

def test_parse_raises_value_error_when_sections_provided_with_base_parser():
    """parse should raise ValueError if a BaseParser is supplied with non‑None sections."""
    with pytest.raises(ValueError) as exc:
        parse("sample text", style=BaseParser(), sections=[1])
    assert str(exc.value) == "A parser has its sections; pass none"

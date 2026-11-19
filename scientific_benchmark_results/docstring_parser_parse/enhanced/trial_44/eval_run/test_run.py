import pytest
from docstring_parser.parser import parse, SectionSpec
from docstring_parser.common import BaseParser, Kind

def test_parse_raises_value_error_when_sections_provided_with_parser():
    """parse should raise ValueError if a BaseParser is given with sections."""
    dummy_section = SectionSpec(titles="param", kind=Kind.PARAM)
    with pytest.raises(ValueError):
        parse("dummy text", style=BaseParser(), sections=[dummy_section])

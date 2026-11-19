import pytest
from docstring_parser.parser import parse
from docstring_parser.common import BaseParser, Kind
from docstring_parser._sections import SectionSpec

def test_parse_value_error_on_sections_with_baseparser():
    style = BaseParser()
    sections = [SectionSpec(titles="param", kind=Kind.PARAM)]
    with pytest.raises(ValueError):
        parse("dummy text", style=style, sections=sections)

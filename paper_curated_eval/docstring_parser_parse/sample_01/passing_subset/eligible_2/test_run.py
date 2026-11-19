import pytest
from docstring_parser.parser import parse, SectionSpec
from docstring_parser.common import BaseParser, Kind

def test_parse_raises_value_error_when_sections_provided_with_parser():
    # Arrange: create a BaseParser instance and a dummy SectionSpec
    parser = BaseParser()
    sections = [SectionSpec(titles="Test", kind=Kind.PARAM)]
    # Act & Assert: passing sections with a parser should raise ValueError
    with pytest.raises(ValueError) as excinfo:
        parse("sample text", style=parser, sections=sections)
    assert "A parser has its sections" in str(excinfo.value)

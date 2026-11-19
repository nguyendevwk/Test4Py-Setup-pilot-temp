import pytest
from docstring_parser.parser import parse, DocstringStyle
from docstring_parser.parsers import BaseParser


class DummyParser(BaseParser):
    def parse(self, text):
        return "parsed"


def test_parse_raises_value_error_when_sections_provided_with_parser_instance():
    dummy = DummyParser()
    with pytest.raises(ValueError) as excinfo:
        parse("some docstring", style=dummy, sections=["section"])
    assert str(excinfo.value) == "A parser has its sections; pass none"

import pytest
from docstring_parser.parser import parse, BaseParser


def test_parse_raises_value_error_when_sections_provided_with_parser_instance():
    class DummyParser(BaseParser):
        def parse(self, text):
            return None

    dummy_parser = DummyParser()
    with pytest.raises(ValueError, match="A parser has its sections; pass none"):
        parse("example docstring", style=dummy_parser, sections=[1])

import pytest
from docstring_parser.parser import parse
from docstring_parser.parsers import BaseParser


def test_parse_with_baseparser_and_sections_raises_value_error():
    class DummyParser(BaseParser):
        def parse(self, text):
            return None

    dummy_parser = DummyParser()
    with pytest.raises(ValueError):
        parse("example docstring", dummy_parser, sections=("section",))

import pytest
from docstring_parser.parser import parse
from docstring_parser.common import BaseParser


def test_parse_raises_value_error_when_parser_and_sections_provided():
    class DummyParser(BaseParser):
        def parse(self, text):
            # Minimal implementation; not used in this test
            return None

    dummy_parser = DummyParser()
    with pytest.raises(ValueError) as exc:
        parse("sample docstring", style=dummy_parser, sections=[1])
    assert str(exc.value) == "A parser has its sections; pass none"

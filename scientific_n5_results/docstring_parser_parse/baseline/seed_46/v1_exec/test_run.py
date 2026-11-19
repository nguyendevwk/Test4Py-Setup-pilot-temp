import pytest
from docstring_parser.parser import parse, BaseParser


def test_parse_with_baseparser_and_sections_raises():
    class DummyParser(BaseParser):
        def parse(self, text):
            return None

    dummy_parser = DummyParser()
    with pytest.raises(ValueError) as exc:
        parse("example docstring", style=dummy_parser, sections=[1])
    assert str(exc.value) == "A parser has its sections; pass none"

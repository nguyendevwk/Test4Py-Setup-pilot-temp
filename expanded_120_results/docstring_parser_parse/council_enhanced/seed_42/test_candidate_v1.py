import pytest
from docstring_parser.parser import parse, DocstringStyle, BaseParser
from docstring_parser.common import Docstring


def test_parse_raises_value_error_when_sections_provided_with_parser_instance():
    class DummyParser(BaseParser):
        def parse(self, text):
            return Docstring(style=DocstringStyle.GOOGLE)

    dummy_parser = DummyParser()
    with pytest.raises(ValueError) as exc:
        parse("sample docstring", style=dummy_parser, sections=[1])
    assert str(exc.value) == "A parser has its sections; pass none"

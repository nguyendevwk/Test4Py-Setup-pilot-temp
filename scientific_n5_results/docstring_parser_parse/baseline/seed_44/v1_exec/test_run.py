import pytest
from docstring_parser.parser import parse, BaseParser, DocstringStyle


class DummyParser(BaseParser):
    def parse(self, text: str):
        return None


def test_parse_raises_value_error_when_sections_provided_with_parser():
    with pytest.raises(ValueError) as excinfo:
        parse("example docstring", style=DummyParser(), sections=["section"])
    assert str(excinfo.value) == "A parser has its sections; pass none"

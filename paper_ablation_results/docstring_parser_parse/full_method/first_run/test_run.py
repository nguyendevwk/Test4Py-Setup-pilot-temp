import pytest
from docstring_parser.parser import parse
from docstring_parser.common import BaseParser, Docstring


def test_parse_raises_value_error_when_sections_provided_with_baseparser():
    """`parse` should raise ValueError if a BaseParser is given with non‑None sections."""
    class DummyParser(BaseParser):
        def parse(self, text: str | None) -> Docstring:
            return Docstring()

    dummy = DummyParser()
    with pytest.raises(ValueError, match="A parser has its sections; pass none"):
        parse("some text", style=dummy, sections=[("Example",)])

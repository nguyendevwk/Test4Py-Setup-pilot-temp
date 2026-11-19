import pytest
from docstring_parser.parser import parse, BaseParser


class DummyParser(BaseParser):
    """Simple parser that returns a constant value."""

    def parse(self, text: str):
        return "dummy"


def test_parse_raises_value_error_when_sections_provided_with_parser_instance():
    """`parse` should raise ValueError if a parser instance is given with sections."""
    dummy_parser = DummyParser()
    with pytest.raises(ValueError):
        parse("example text", style=dummy_parser, sections=[("section", "type")])

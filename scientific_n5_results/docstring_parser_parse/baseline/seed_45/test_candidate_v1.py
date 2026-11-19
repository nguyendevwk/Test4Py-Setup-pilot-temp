import pytest
from docstring_parser.parser import parse, BaseParser


class DummyParser(BaseParser):
    """A minimal concrete parser for testing purposes."""

    def parse(self, text):
        # The implementation is irrelevant for this test; it will never be called.
        return None


def test_parse_raises_value_error_when_sections_provided_with_parser_instance():
    """`parse` should raise ValueError if a parser instance is supplied with non‑None sections."""
    dummy_parser = DummyParser()
    with pytest.raises(ValueError):
        parse("example docstring", style=dummy_parser, sections=["section"])

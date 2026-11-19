import pytest
from docstring_parser.parser import parse
from docstring_parser.common import BaseParser, Docstring, ParseResult


class DummyParser(BaseParser):
    """A minimal parser that satisfies BaseParser's interface."""

    def try_parse(self, text):
        # Return a successful parse result with an empty Docstring.
        return ParseResult(Docstring(), [])


def test_parse_raises_value_error_when_sections_provided_with_baseparser():
    """`parse` should raise ValueError if a BaseParser instance is given with sections."""
    dummy_parser = DummyParser()
    # Any non‑None value for sections triggers the error.
    with pytest.raises(ValueError, match="A parser has its sections"):
        parse("sample text", style=dummy_parser, sections=[1])

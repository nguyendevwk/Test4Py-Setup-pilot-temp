import pytest
from docstring_parser.parser import parse, BaseParser, DocstringStyle
from docstring_parser.common import Docstring


def test_parse_with_baseparser_and_sections():
    """Verify that passing a BaseParser instance behaves correctly."""
    class DummyParser(BaseParser):
        def parse(self, text: str | None) -> Docstring:
            # Return a Docstring with a known style for assertion.
            return Docstring(style=DocstringStyle.GOOGLE)

    dummy = DummyParser()
    # When sections is None, parse should delegate to the parser's parse method.
    result = parse("sample text", style=dummy, sections=None)
    assert isinstance(result, Docstring)
    assert result.style == DocstringStyle.GOOGLE

    # When sections is provided, a ValueError should be raised.
    with pytest.raises(ValueError, match="A parser has its sections"):
        parse("sample text", style=dummy, sections=())

import pytest
from docstring_parser.parser import parse
from docstring_parser.common import BaseParser, Docstring


def test_parse_raises_value_error_when_sections_provided_with_parser():
    """parse should raise ValueError if a BaseParser instance is given with sections."""
    class DummyParser(BaseParser):
        def parse(self, text):
            # Return a minimal Docstring instance for completeness
            return Docstring()

    dummy_parser = DummyParser()
    with pytest.raises(ValueError) as exc:
        parse("sample text", style=dummy_parser, sections=[1])
    assert str(exc.value) == "A parser has its sections; pass none"

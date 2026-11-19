import pytest
from docstring_parser.parser import parse, BaseParser


def test_parse_raises_value_error_when_style_is_parser_and_sections_provided():
    class DummyParser(BaseParser):
        def parse(self, text):
            # This should never be called in this test
            raise RuntimeError("parse should not be invoked")

    dummy_parser = DummyParser()
    with pytest.raises(ValueError):
        parse("example docstring", style=dummy_parser, sections=("custom_section",))

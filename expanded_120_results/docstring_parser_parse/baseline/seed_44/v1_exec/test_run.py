import pytest
from docstring_parser.parser import parse
from docstring_parser.parsers import BaseParser


def test_parse_raises_value_error_when_sections_provided_with_parser():
    """parse should raise ValueError if a BaseParser is given with non‑None sections."""
    class DummyParser(BaseParser):
        def parse(self, text):
            # Dummy implementation; not used in this test
            return None

    dummy_parser = DummyParser()
    with pytest.raises(ValueError) as excinfo:
        parse("example docstring", style=dummy_parser, sections=("section",))
    assert str(excinfo.value) == "A parser has its sections; pass none"

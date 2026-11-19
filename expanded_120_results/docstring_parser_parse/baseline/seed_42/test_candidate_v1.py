import pytest
from docstring_parser.parser import parse, BaseParser


class DummyParser(BaseParser):
    """Minimal parser implementation for testing."""

    def parse(self, text: str):
        # Return a dummy Docstring object; the actual value is irrelevant for this test.
        return None


def test_parse_raises_value_error_when_sections_provided_with_parser_instance():
    """
    Verify that providing a BaseParser instance together with a non‑None
    ``sections`` argument raises a ValueError with the expected message.
    """
    dummy_parser = DummyParser()
    with pytest.raises(ValueError) as excinfo:
        parse("sample text", style=dummy_parser, sections=["section"])
    assert str(excinfo.value) == "A parser has its sections; pass none"

import pytest
from docstring_parser.parser import parse
from docstring_parser.common import BaseParser


def test_parse_raises_value_error_when_sections_provided_with_baseparser():
    """
    Passing a BaseParser instance with a non‑None sections argument
    should raise ValueError, as the parser already defines its sections.
    """
    parser = BaseParser()
    # Any non‑None value for sections triggers the error
    with pytest.raises(ValueError):
        parse("sample text", style=parser, sections=[1])

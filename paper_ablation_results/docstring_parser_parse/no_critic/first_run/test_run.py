import pytest
from docstring_parser.parser import parse
from docstring_parser.common import BaseParser


def test_parse_raises_value_error_when_sections_provided_with_baseparser():
    """parse should raise ValueError if a BaseParser instance is given with sections."""
    # A BaseParser instance is accepted as a style, but sections must be None.
    base_parser = BaseParser()
    with pytest.raises(ValueError):
        parse("sample text", style=base_parser, sections=[1])

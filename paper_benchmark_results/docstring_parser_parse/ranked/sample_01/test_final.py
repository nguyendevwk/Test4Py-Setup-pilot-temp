import pytest
from docstring_parser.parser import parse, BaseParser


def test_parse_raises_value_error_when_sections_provided_with_baseparser():
    """
    When a BaseParser instance is supplied as the style and sections are also
    provided, parse should raise a ValueError before attempting to parse.
    """
    with pytest.raises(ValueError):
        parse("dummy text", style=BaseParser(), sections=[1])

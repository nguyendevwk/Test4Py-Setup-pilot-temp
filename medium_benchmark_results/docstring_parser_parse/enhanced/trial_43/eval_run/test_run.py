import pytest
from docstring_parser.parser import parse
from docstring_parser.common import BaseParser

def test_parse_raises_value_error_when_sections_provided_with_parser():
    with pytest.raises(ValueError) as exc:
        parse("some text", style=BaseParser(), sections=[])
    assert str(exc.value) == "A parser has its sections; pass none"

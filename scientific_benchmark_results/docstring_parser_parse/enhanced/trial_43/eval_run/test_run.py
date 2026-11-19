import pytest
from docstring_parser.parser import parse
from docstring_parser.common import BaseParser

sample_doc = """Summary line.

:param name: param desc
:type name: str
:returns: return desc
"""

def test_parse_raises_value_error_when_sections_provided_with_parser():
    """`parse` should raise ValueError if a BaseParser instance is given with sections."""
    with pytest.raises(ValueError) as exc:
        parse(sample_doc, style=BaseParser(), sections=[1])
    assert str(exc.value) == "A parser has its sections; pass none"

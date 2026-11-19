import pytest
from docstring_parser.common import Docstring

def test_description_with_short_and_blank_and_long():
    d = Docstring()
    d.short_description = "Short"
    d.blank_after_short_description = True
    d.long_description = "Long"
    expected = "Short\n\nLong"
    assert d.description == expected

def test_description_none_when_no_parts():
    d = Docstring()
    assert d.description is None

def test_meta_lists_are_empty_by_default():
    d = Docstring()
    assert d.params == []
    assert d.raises == []
    assert d.many_returns == []
    assert d.examples == []
    assert d.deprecation is None

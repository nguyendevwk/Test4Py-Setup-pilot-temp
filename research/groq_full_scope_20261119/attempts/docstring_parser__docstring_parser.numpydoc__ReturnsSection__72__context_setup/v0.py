import inspect
import re
import pytest
from docstring_parser.numpydoc import ReturnsSection, RETURN_KEY_REGEX, _clean_str
from docstring_parser.numpydoc.common import DocstringReturns

def test_parse_item_without_name_and_type():
    """When key contains only a type, name should be None."""
    section = ReturnsSection(title="Returns", key="returns")
    # key matches regex with only type
    key = "int"
    value = "An integer value."
    result = section._parse_item(key, value)
    assert isinstance(result, DocstringReturns)
    assert result.return_name is None
    assert result.type_name == "int"
    assert result.description == "An integer value."
    assert result.args == ["returns"]
    assert result.is_generator is False

def test_parse_item_with_name_and_type():
    """When key contains name and type, both should be captured."""
    section = ReturnsSection(title="Returns", key="returns")
    key = "count : int"
    value = "Number of items."
    result = section._parse_item(key, value)
    assert isinstance(result, DocstringReturns)
    assert result.return_name == "count"
    assert result.type_name == "int"
    assert result.description == "Number of items."
    assert result.args == ["returns"]
    assert result.is_generator is False

def test_clean_str_trims_and_returns_none_on_empty():
    """_clean_str should strip whitespace and return None for empty strings."""
    assert _clean_str("  hello  ") == "hello"
    assert _clean_str("") is None
    assert _clean_str("   ") is None

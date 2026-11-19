import re
import pytest
from docstring_parser.numpydoc import ReturnsSection
from docstring_parser.numpydoc.common import DocstringReturns

# Helper to create a ReturnsSection instance with a dummy key
def make_section(key: str):
    section = ReturnsSection()
    section.key = key
    return section

def test_parse_item_with_name_and_type():
    """Normal case: key contains name and type."""
    section = make_section("value : int")
    result = section._parse_item(section.key, "An integer value.")
    assert isinstance(result, DocstringReturns)
    assert result.return_name == "value"
    assert result.type_name == "int"
    assert result.description == "An integer value."
    assert result.args == ["value : int"]
    assert result.is_generator is False

def test_parse_item_without_name():
    """Boundary case: key contains only type, no name."""
    section = make_section("float")
    result = section._parse_item(section.key, "A floating point number.")
    assert isinstance(result, DocstringReturns)
    assert result.return_name is None
    assert result.type_name == "float"
    assert result.description == "A floating point number."
    assert result.args == ["float"]
    assert result.is_generator is False

def test_parse_item_invalid_key():
    """Error case: key does not match expected pattern."""
    section = make_section("invalid key")
    result = section._parse_item(section.key, "Should still parse.")
    assert isinstance(result, DocstringReturns)
    assert result.return_name is None
    assert result.type_name is None
    assert result.description == "Should still parse."
    assert result.args == ["invalid key"]
    assert result.is_generator is False

import re
import pytest
from docstring_parser.numpydoc import ReturnsSection
from docstring_parser.numpydoc.common import DocstringReturns

# Helper regex from the module (re-exported for clarity)
RETURN_KEY_REGEX = re.compile(r"(?P<name>[\w\.]+)?\s*:\s*(?P<type>.+)")

def test_parse_item_with_name_and_type():
    """Normal case: key contains name and type."""
    section = ReturnsSection(title="Returns", key="value : int")
    result = section._parse_item(section.key, "   The returned integer.")
    assert isinstance(result, DocstringReturns)
    assert result.return_name == "value"
    assert result.type_name == "int"
    assert result.args == ["Returns"]
    # description should be cleaned of leading whitespace
    assert result.description == "The returned integer."

def test_parse_item_without_name():
    """Boundary case: key contains only type, no name."""
    section = ReturnsSection(title="Returns", key="float")
    result = section._parse_item(section.key, "   A floating point number.")
    assert isinstance(result, DocstringReturns)
    assert result.return_name is None
    assert result.type_name == "float"
    assert result.args == ["Returns"]
    assert result.description == "A floating point number."

def test_parse_item_invalid_key():
    """Error case: key does not match the expected pattern."""
    section = ReturnsSection(title="Returns", key="invalid key")
    result = section._parse_item(section.key, "   Some description.")
    assert isinstance(result, DocstringReturns)
    # When regex fails, both name and type should be None
    assert result.return_name is None
    assert result.type_name is None
    assert result.args == ["Returns"]
    assert result.description == "Some description."

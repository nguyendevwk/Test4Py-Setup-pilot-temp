import re
import inspect
import pytest
from docstring_parser.numpydoc import ReturnsSection
from docstring_parser.numpydoc.common import DocstringReturns

# Helper to access the private regex used by ReturnsSection
RETURN_KEY_REGEX = re.compile(
    r"(?P<name>\w+)\s*:\s*(?P<type>.+)"
)

def test_parse_item_with_name_and_type():
    """Normal case: key contains a name and a type."""
    section = ReturnsSection()
    key = "value : int"
    value = "  The value returned by the function.  "
    result = section._parse_item(key, value)

    assert isinstance(result, DocstringReturns)
    assert result.return_name == "value"
    assert result.type_name == "int"
    assert result.description == "The value returned by the function."
    assert result.is_generator is False
    assert result.args == ["returns"]

def test_parse_item_without_name():
    """Boundary case: key contains only a type, no name."""
    section = ReturnsSection()
    key = "float"
    value = "A floating point number."
    result = section._parse_item(key, value)

    assert isinstance(result, DocstringReturns)
    assert result.return_name is None
    assert result.type_name == "float"
    assert result.description == "A floating point number."
    assert result.is_generator is False
    assert result.args == ["returns"]

def test_parse_item_generator_flag_and_cleaning():
    """Error/edge case: generator flag and description cleaning."""
    section = ReturnsSection()
    section.is_generator = True
    key = "data : list"
    value = "\n    List of data points.\n"
    result = section._parse_item(key, value)

    assert isinstance(result, DocstringReturns)
    assert result.is_generator is True
    assert result.description == "List of data points."
    assert result.type_name == "list"
    assert result.return_name == "data"

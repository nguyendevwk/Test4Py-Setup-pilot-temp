import inspect
import pytest
from docstring_parser.numpydoc import ReturnsSection, RETURN_KEY_REGEX, DocstringReturns

def test_parse_item_with_name_and_type():
    section = ReturnsSection(title="Returns", key="return")
    # key includes name and type
    key = "value : int"
    value = "An integer value."
    result = section._parse_item(key, value)
    assert isinstance(result, DocstringReturns)
    assert result.return_name == "value"
    assert result.type_name == "int"
    assert result.description == "An integer value."
    assert result.is_generator is False
    assert result.args == ["return"]

def test_parse_item_without_name():
    section = ReturnsSection(title="Returns", key="return")
    # key includes only type
    key = "float"
    value = "A floating point number."
    result = section._parse_item(key, value)
    assert result.return_name is None
    assert result.type_name == "float"
    assert result.description == "A floating point number."

def test_parse_item_empty_value_and_generator_flag():
    section = ReturnsSection(title="Returns", key="return")
    section.is_generator = True
    key = "data : list"
    value = "   "  # empty after stripping
    result = section._parse_item(key, value)
    assert result.description is None
    assert result.is_generator is True
    assert result.type_name == "list"
    assert result.return_name == "data"

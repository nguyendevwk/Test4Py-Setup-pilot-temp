import re
import pytest
from docstring_parser.numpydoc import ReturnsSection, RETURN_KEY_REGEX
from docstring_parser.common import DocstringReturns

def test_parse_item_with_valid_key_and_description(tmp_path):
    """Verify that a correctly formatted key yields the expected DocstringReturns."""
    section = ReturnsSection(title="Returns", key="return_value")
    key = "value : int"
    value = "   The integer value returned.\n   It is positive."
    result = section._parse_item(key, value)

    assert isinstance(result, DocstringReturns)
    assert result.args == ["return_value"]
    assert result.return_name == "value"
    assert result.type_name == "int"
    assert result.is_generator is False
    # description should be cleaned: leading/trailing whitespace removed, internal newlines collapsed
    assert result.description == "The integer value returned.\nIt is positive."

def test_parse_item_with_missing_name_and_type(tmp_path):
    """When the key does not match the regex, name and type should be None."""
    section = ReturnsSection(title="Returns", key="return_value")
    key = "just a description"
    value = "No type or name provided."
    result = section._parse_item(key, value)

    assert isinstance(result, DocstringReturns)
    assert result.return_name is None
    assert result.type_name is None
    assert result.description == "No type or name provided."

def test_parse_item_with_complex_type_and_multiline_description(tmp_path):
    """Test parsing of a key with a complex type and a multiline description."""
    section = ReturnsSection(title="Returns", key="return_value")
    key = "data : List[Dict[str, Any]]"
    value = """
        The data structure returned.
        It contains a list of dictionaries.
        Each dictionary maps strings to any type.
    """
    result = section._parse_item(key, value)

    assert isinstance(result, DocstringReturns)
    assert result.return_name == "data"
    assert result.type_name == "List[Dict[str, Any]]"
    # description should be cleaned: leading/trailing whitespace removed, internal newlines collapsed
    expected_description = (
        "The data structure returned.\n"
        "It contains a list of dictionaries.\n"
        "Each dictionary maps strings to any type."
    )
    assert result.description == expected_description

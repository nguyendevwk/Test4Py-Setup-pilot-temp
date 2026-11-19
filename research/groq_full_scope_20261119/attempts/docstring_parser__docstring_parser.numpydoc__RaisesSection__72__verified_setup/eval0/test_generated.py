import pytest
from docstring_parser.numpydoc import RaisesSection
from docstring_parser.common import DocstringRaises

def test_parse_item_basic():
    """Basic parsing of a normal raises entry."""
    section = RaisesSection()
    result = section._parse_item("ValueError", "An error occurs when input is invalid.")
    assert isinstance(result, DocstringRaises)
    assert result.args == ["RaisesSection", "ValueError"]
    assert result.type_name == "ValueError"
    # description should be cleaned (leading/trailing whitespace removed)
    assert result.description == "An error occurs when input is invalid."

def test_parse_item_empty_key():
    """When the key is an empty string, type_name should be None."""
    section = RaisesSection()
    result = section._parse_item("", "No exception type specified.")
    assert isinstance(result, DocstringRaises)
    assert result.args == ["RaisesSection", ""]
    assert result.type_name is None
    assert result.description == "No exception type specified."

def test_parse_item_description_cleaning():
    """Description should be cleaned of leading/trailing whitespace and newlines."""
    section = RaisesSection()
    raw_description = "\n    This error\n    occurs when\n    something bad happens.\n"
    result = section._parse_item("RuntimeError", raw_description)
    expected = "This error\noccurs when\nsomething bad happens."
    assert result.description == expected

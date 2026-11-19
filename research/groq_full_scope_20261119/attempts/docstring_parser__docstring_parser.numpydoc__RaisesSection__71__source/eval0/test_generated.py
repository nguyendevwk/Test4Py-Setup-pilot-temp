import pytest
from docstring_parser.numpydoc import RaisesSection
from docstring_parser.common import DocstringRaises

def test_parse_item_normal():
    section = RaisesSection()
    key = "ValueError"
    value = "  This error occurs when the input is invalid.  "
    result = section._parse_item(key, value)
    assert isinstance(result, DocstringRaises)
    assert result.args == ["RaisesSection", key]
    assert result.type_name == key
    # description should be stripped of leading/trailing whitespace
    assert result.description == "This error occurs when the input is invalid."

def test_parse_item_empty_key():
    section = RaisesSection()
    key = ""
    value = "An error with no explicit type name."
    result = section._parse_item(key, value)
    assert isinstance(result, DocstringRaises)
    assert result.args == ["RaisesSection", key]
    assert result.type_name is None
    assert result.description == "An error with no explicit type name."

def test_parse_item_multiline_description():
    section = RaisesSection()
    key = "RuntimeError"
    value = """
        First line of description.
        Second line with indentation.
        Third line.
    """
    result = section._parse_item(key, value)
    # description should be cleaned: leading/trailing newlines removed, indentation collapsed
    expected = "First line of description.\nSecond line with indentation.\nThird line."
    assert result.description == expected
